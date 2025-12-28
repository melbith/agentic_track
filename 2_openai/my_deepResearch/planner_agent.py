from pydantic import BaseModel, Field
from agents import Agent


# Use Pydantic to define the Schema of our response - this is known as "Structured Outputs"

class WebSearchItem(BaseModel):
    reason: str = Field(description="Your reasoning for why this search is important to the query.")
    query: str = Field(description="The search term to use for the web search.")

class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem] = Field(description="A list of web searches to perform to best answer the query.")

# Set the number of searches to perform. Unless limited, this can add upto bigger Web Search costs

SEARCH_COUNT = 5

PA_INSTRUCTIONS = f"You are a helpful research assistant. Given a query, come up with a set of web searches \
to perform to best answer the query. Output {SEARCH_COUNT} terms to query for."

planner_agent = Agent(
    name="Planner Agent",
    instructions=PA_INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=WebSearchPlan,
)