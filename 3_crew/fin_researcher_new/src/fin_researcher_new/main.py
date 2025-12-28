#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from fin_researcher_new.crew import ResearchCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the Researcher crew.
    """
    inputs = {
        'company': 'Tesla',
        # 'current_year': str(datetime.now().year)
    }

    try:
        result = ResearchCrew().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


    print("\n\n=== FINAL REPORT ===\n\n")
    print(result.raw)

    print("\n\nReport has been saved to output/report.md")

    

if __name__ == "__main__":
    run()



