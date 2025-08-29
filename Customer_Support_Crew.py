import os
from crewai import Crew
from Agents import Agents
from Task import SupportTask
from rich.console import Console
from rich.markdown import Markdown
from Log import *


agents = Agents()
tasks = SupportTask()

# ---- build agents once ----
support_rep = agents.support_agent()
quality_assurance = agents.support_quality_assurance_agent()

# ---- build tasks once ----
inquiry_task_rep = tasks.inquiry_task
quality_assurance_task = tasks.quality_assurance_task

# ---- assemble Crew ----
crew = Crew(
    agents=[support_rep, quality_assurance],
    tasks=[inquiry_task_rep, quality_assurance_task],
    verbose=False,
    memory=True,
)

if __name__ == "__main__":
    # sanity check for API key (avoids confusing network errors later)
    try:
        if not os.getenv("OPENAI_API_KEY"):
            print("[WARN] OPENAI_API_KEY is not set in the environment.")

        customer = input("Please enter customer ID: ")
        person = input("Please enter your first name: ")
        inquiry = input("How can I help you?: ")


        result = crew.kickoff(inputs={"customer": customer,
                                      "person": person,
                                      "inquiry": inquiry}      )
        # Ensure printable string
        result_str = result if isinstance(result, str) else str(result)

         # Pretty terminal preview
        Console().print(Markdown(result_str))
    except Exception as e:
        LOGGER.error(e)
        LOGGER.exception(f"Unhandled exception occurred: {e}")