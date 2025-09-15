from crewai import Crew
from rich.console import Console
from rich.markdown import Markdown
from Agents import JobAgents
from Task import JobApplication
from Log import *


agents = JobAgents()
tasks = JobApplication()

# ---- build agents once ----
researcher= agents.resume_researcher_agent()
profiler = agents.profiler_agent()
resume_strategist = agents.resume_strategist_agent()
interview_preparer = agents.interview_preparation_agent()

# ---- build tasks once ----
research_task= tasks.research_task
profiler_task= tasks.profile_task
resume_strategist_task= tasks.resume_strategy_task
interview_preparer_task= tasks.interview_preparation_task

# ---- assemble Crew ----
job_application_crew = Crew(
    agents=[researcher, profiler, resume_strategist, interview_preparer, ],
    tasks=[research_task, profiler_task, resume_strategist_task, interview_preparer_task],
    verbose=True,
)

job_application_inputs = {
    'job_posting_url': 'https://www.simplyhired.com/job/E3SMVgo5Qkqrhoyx-ooLCz21JhH8y3KKxZoo9TIzsD3qunQ3dls_gw?utm_campaign=google_jobs_apply&utm_source=google_jobs_apply&utm_medium=organic',
    'github_url': 'https://github.com/Godson90',
    'linkedin_url': 'https://www.linkedin.com/in/adesola-adeola-5255841b7/',
    'personal_writeup': """Gabriel is an accomplished Cybersecurity Analyst with 5 years of experience, specializing in
    managing remote and in-office teams, and expert in multiple
    programming languages and frameworks. He holds an Bachelor's degree and a strong
    background in AI and Information security. Gabriel has successfully implemented major projects, proving his 
    ability to drive Cybersecurity goals and development. Ideal for senior analyst 
    roles that require a technical and leadership approach.""" }

if __name__ == "__main__":
    result = job_application_crew.kickoff(inputs=job_application_inputs)
    # Ensure printable string
    result_str = result if isinstance(result, str) else str(result)
    # Pretty terminal preview
    Console().print(Markdown("./tailored_resume.md"))
    Console().print(Markdown("./interview_materials.md"))