# tasks.py
import  os
from __future__ import annotations
from typing import List, Optional
from crewai import Task
from crewai_tools import ScrapeWebsiteTool, DirectoryReadTool, FileReadTool, SerperDevTool
from Agents import Agents, JobAgents
from Sentiment_Analysis import SentimentAnalysis
from Custom_Models import VenueDetails
from config import task_config


class ContentTasks:
    """
    Factory that builds and holds the three CrewAI tasks for your content workflow:
    - plan_task  -> planner agent
    - write_task -> writer agent (depends on plan_task)
    - edit_task  -> editor agent (depends on write_task)

    The {topic} placeholder in descriptions is filled by Crew inputs at kickoff.
    """

    def __init__(self, agents: Optional[object] = None) -> None:
        # Cache a single agents provider (so we don't recreate agents repeatedly)
        self._agents = Agents()

        # Build tasks once and wire up contexts in order
        self.plan_task: Task = Task(
            config=task_config()['plan_task'],
            agent=self._agents.planner(),
        )

        self.write_task: Task = Task(
            config=task_config()['write_task'],
            agent=self._agents.writer(),
            context=[self.plan_task],  # <-- reference the already-built plan_task
        )

        self.edit_task: Task = Task(
            config=task_config()['edit_task'],
            agent=self._agents.editor(),
            context=[self.write_task],  # <-- reference the already-built write_task
        )

    def all(self) -> List[Task]:
        """Return tasks in execution order (plan → write → edit)."""
        return [self.plan_task, self.write_task, self.edit_task]

class SupportTask:


    def __init__(self, agents: Optional[object] = None) -> None:
        self._agents = Agents()
        self._scrape_website_tool = ScrapeWebsiteTool(website_url="https://www.defenstack.com")

        self.inquiry_task: Task =  Task(
            config=task_config()['inquiry_task'],
            tools=[self._scrape_website_tool],
            agent=self._agents.support_agent(),
            )


        self.quality_assurance_task: Task = Task(
            config=task_config()['quality_assurance_task'],
            agent=self._agents.support_quality_assurance_agent(),
        )

class CustomerOutreach:

    def __init__(self, agents: Optional[object] = None) -> None:
        self._agents = Agents()
        self._directory_read_tool = DirectoryReadTool(directory='./instructions')
        self._file_read_tool = FileReadTool()
        self._search_tool = SerperDevTool()
        self._sentiment_analysis_tool = SentimentAnalysis()

        self.lead_profiling_task = Task(
            config=task_config()['lead_profiling_task'],
            tools=[self._directory_read_tool, self._file_read_tool,self._search_tool,],
            agent=self._agents.sales_rep_agent(),
        )

        self.personalized_outreach_task = Task(
           config=task_config()['personalized_outreach_task'],
            tools=[self._sentiment_analysis_tool, self._search_tool],
            agent=self._agents.lead_sales_rep_agent(),
        )

class EventPlanner:
    def __init__(self, agents: Optional[object] = None) -> None:
        self._agents = Agents()

        self.venue_task = Task(
           config=task_config()['venue_task'],
            human_input=True,
            output_json=VenueDetails,
            output_file="venue_details.json",
             # output the venue details as a JSON File
            agent=self._agents.venue_cordinator_agent(),
        )

        self.marketing_task = Task(
           config=task_config()['marketing_task'],
            output_file="marketing_report.md",
            agent=self._agents.marketing_communication_agent(),
        )
        self.logistics_task = Task(
            config=task_config()['logistics_task'],
            human_input=True,
            async_execution=True,
            agent=self._agents.logistic_manager_agent(),
        )

class JobApplication:
    def __init__(self, agents: Optional[object] = None) -> None:
        self._agents = JobAgents()

        self.research_task = Task(
            config=task_config()['research_task'],
            agent=self._agents.resume_researcher_agent(),
            async_execution=True
        )

        self.profile_task = Task(
            config=task_config()['profile_task'],
            agent=self._agents.profiler_agent(),
            async_execution=True
        )

        self.resume_strategy_task = Task(
            config=task_config()['resume_strategy_task'],
            output_file="tailored_resume.md",
            context=[self.research_task, self.profile_task],
            agent=self._agents.resume_strategist_agent()
        )

        self.interview_preparation_task = Task(
            config=task_config()['interview_preparation_task'],
            output_file="interview_materials.md",
            context=[self.research_task, self.profile_task, self.resume_strategy_task],
            agent=self._agents.interview_preparation_agent()
        )