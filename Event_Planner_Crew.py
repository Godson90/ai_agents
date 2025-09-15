import json
from crewai import Crew
from rich.console import Console
from rich.markdown import Markdown
from Agents import Agents
from Task import EventPlanner
from Log import *
from pprint import pprint

agents = Agents()
tasks = EventPlanner()

# ---- build agents once ----
venue_coordinator= agents.venue_cordinator_agent()
logistic_manager= agents.logistic_manager_agent()
marketing_communicator= agents.marketing_communication_agent()

# ---- build tasks once ----
venue = tasks.venue_task
logistics = tasks.logistics_task
marketing = tasks.marketing_task

# ---- assemble Crew ----
crew = Crew(
    agents=[venue_coordinator, marketing_communicator,  logistic_manager],
    tasks=[venue,marketing,logistics],
    verbose=True,
    memory=True,
)

if __name__ == "__main__":
    event_details = {
        'event_topic': "Tech Innovation Conference",
        'event_description': "A gathering of tech innovators "
                             "and industry leaders "
                             "to explore future technologies.",
        'event_city': "Lewis Center OH",
        'tentative_date': "2025-09-20",
        'expected_participants': 50,
        'budget': 5000,
        'venue_type': "Conference Hall"
    }
    result = crew.kickoff(inputs=event_details)
    # Ensure printable string
    result_str = result if isinstance(result, str) else str(result)
    # Pretty terminal preview
    Console().print(Markdown(result_str))
    with open('venue_details.json') as f:
        venue_data = json.load(f)
    pprint(venue_data)