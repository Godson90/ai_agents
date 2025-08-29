from crewai import Crew
from rich.console import Console
from rich.markdown import Markdown
from Agents import Agents
from Task import CustomerOutreach
from Log import *


agents = Agents()
tasks = CustomerOutreach()

# ---- build agents once ----
sales_rep= agents.sales_rep_agent()
lead_sales_rep = agents.lead_sales_rep_agent()

# ---- build tasks once ----
lead_profiler= tasks.lead_profiling_task
personalized_outreach = tasks.personalized_outreach_task

# ---- assemble Crew ----
crew = Crew(
    agents=[sales_rep, lead_sales_rep],
    tasks=[lead_profiler, personalized_outreach],
    verbose=False,
    memory=True,
)

if __name__ == "__main__":
    os.environ['SERPER_API_KEY'] = os.getenv('SERPER_API_KEY')
    inputs = {
        "lead_name": "Defenstack",
        "industry": "Cybersecurity",
        "key_decision_maker": "Gabriel Adeola",
        "position": "CEO",
        "milestone": "product launch"
    }

    result = crew.kickoff(inputs=inputs)
    # Ensure printable string
    result_str = result if isinstance(result, str) else str(result)
    # Pretty terminal preview
    Console().print(Markdown(result_str))