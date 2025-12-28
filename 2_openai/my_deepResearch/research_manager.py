import asyncio
from agents import Runner, trace, gen_trace_id

from planner_agent import planner_agent, WebSearchItem, WebSearchPlan
from search_agent import search_agent
from writer_agent import writer_agent, ReportData
from email_agent import email_agent

class ResearchManager:
    """ Contains the 5 coroutines (same as the notebook version but tidied up) to perform 
    the deep research process and the main coroutine to manage the process.
    """

    # Coroutine 1 - to plan the searches to perform for the query
    async def plan_searches(self, query: str) -> WebSearchPlan:
        """ Plan the searches to perform for the query """
        print("Planning searches...")
        result = await Runner.run(planner_agent, f"Query: {query}")
        print(f"Planned to perform {len(result.final_output.searches)} searches")
        return result.final_output_as(WebSearchPlan)


    # Coroutine 2 - to organize the searches to perform for the query and track individual search executions
    async def organize_searches(self, search_plan: WebSearchPlan) -> list[str]:
        """ Organize the searches to perform for the query """
        print("Organizing concurrent search executions...") 
        num_completed = 0
        results = []
        tasks = [asyncio.create_task(self.perform_search(item)) for item in search_plan.searches] # Create a list of tasks to perform the searches

        for task in asyncio.as_completed(tasks):
            result = await task
            if result is not None:
                results.append(result)
            num_completed += 1

            print(f"Searching... {num_completed}/{len(tasks)} completed")

        print("Finished searching")
        return results
    

    # Coroutine 3 - to perform the individual searches. Invoked by the organize_searches coroutine
    async def perform_search(self, item: WebSearchItem) -> str | None:
        """ Use the search agent to run a web search for each item in the search plan """
        input = f"Search Item: {item.query}\nReason for searching: {item.reason}"
        try:
            result = await Runner.run(
                search_agent,
                input,
            )
            return str(result.final_output)
        except Exception:
            return None


    # Coroutine 4 - to write the report based on the search results
    async def write_report(self, query: str, search_results: list[str]) -> ReportData:
        """ Use the writer agent to write a report based on the search results"""
        print("Thinking about report...")

        input = f"Original Query: {query}\nSummarized search results: {search_results}"
        result = await Runner.run(
            writer_agent,
            input,
        )

        print("Finished writing report")
        return result.final_output_as(ReportData)

    
    # Coroutine 5 - to send the email with the report
    async def send_email(self, report: ReportData) -> None:
        """ Use the email agent to send an email with the report """
        print("Writing email...")
        result = await Runner.run(
            email_agent,
            report.markdown_report,
        )
        print("Email sent")
        return report

#--------------------------------------------
# Main coroutine to run the deep research process
#--------------------------------------------
    async def run(self, query: str):
        """ Run the deep research process, yielding the status updates and the final report"""
        
        trace_id = gen_trace_id() # Generate a trace ID to display the trace link

        with trace("Deep Research", trace_id=trace_id):
            print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}")
            yield f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}"

            print("Starting research...")

            search_plan = await self.plan_searches(query)
            yield "Searches planned, starting to search..."

            search_results = await self.organize_searches(search_plan)
            yield "Searches complete, writing report..."

            report = await self.write_report(query, search_results)
            yield "Report written, sending email..."

            await self.send_email(report)
            yield "Email sent, research complete"
            
            yield report.markdown_report
