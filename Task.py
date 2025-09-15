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
            description=(
                "Review the response drafted by the Senior Support Representative for {customer}'s inquiry. "
                "Ensure that the answer is comprehensive, accurate, and adheres to the "
                "high-quality standards expected for customer support.\n"
                "Verify that all parts of the customer's inquiry "
                "have been addressed "
                "thoroughly, with a helpful and friendly tone.\n"
                "Check for references and sources used to "
                " find the information, "
                "ensuring the response is well-supported and "
                "leaves no questions unanswered."
            ),
            expected_output=(
                "A final, detailed, summarized, and informative response "
                "ready to be sent to the customer.\n"
                "This response should fully address the "
                "customer's inquiry, incorporating all "
                "relevant feedback and improvements.\n"
                "Don't be too formal, we are a chill and cool company "
                "but maintain a professional and friendly tone throughout."

            ),
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
            description=(
                "Conduct an in-depth analysis of {lead_name}, "
                "a company in the {industry} sector "
                "that recently showed interest in our solutions. "
                "Utilize all available data sources "
                "to compile a detailed profile, "
                "focusing on key decision-makers, recent business "
                "developments, and potential needs "
                "that align with our offerings. "
                "This task is crucial for tailoring "
                "our engagement strategy effectively.\n"
                "Don't make assumptions and "
                "only use information you absolutely sure about."
            ),
            expected_output=(
                "A comprehensive report on {lead_name}, "
                "including company background, "
                "key personnel, recent milestones, and identified needs. "
                "Highlight potential areas where "
                "our solutions can provide value, "
                "and suggest personalized engagement strategies."
            ),
            tools=[self._directory_read_tool, self._file_read_tool,self._search_tool,],
            agent=self._agents.sales_rep_agent(),
        )

        self.personalized_outreach_task = Task(
            description=(
                "Using the insights gathered from "
                "the lead profiling report on {lead_name}, "
                "craft a personalized outreach campaign "
                "aimed at {key_decision_maker}, "
                "the {position} of {lead_name}. "
                "The campaign should address their recent {milestone} "
                "and how our solutions can support their goals. "
                "Your communication must resonate "
                "with {lead_name}'s company culture and values, "
                "demonstrating a deep understanding of "
                "their business and needs.\n"
                "Don't make assumptions and only "
                "use information you absolutely sure about."
            ),
            expected_output=(
                "A series of personalized email drafts "
                "tailored to {lead_name}, "
                "specifically targeting {key_decision_maker}."
                "Each draft should include "
                "a compelling narrative that connects our solutions "
                "with their recent achievements and future goals. "
                "Ensure the tone is engaging, professional, "
                "and aligned with {lead_name}'s corporate identity."
                "Finally select the best of the series of email drafts."
            ),
            tools=[self._sentiment_analysis_tool, self._search_tool],
            agent=self._agents.lead_sales_rep_agent(),
        )

class EventPlanner:
    def __init__(self, agents: Optional[object] = None) -> None:
        self._agents = Agents()

        self.venue_task = Task(
            description=(
                "Find a venue in {event_city} "
                "that meets criteria for {event_topic}."
            ),
            expected_output=(
                "All the details of a specifically chosen"
                "venue you found to accommodate the event."
            ),
            human_input=True,
            output_json=VenueDetails,
            output_file="venue_details.json",
             # output the venue details as a JSON File
            agent=self._agents.venue_cordinator_agent(),
        )

        self.marketing_task = Task(
            description=(
                "Promote the {event_topic} "
                "aiming to engage at least"
                "{expected_participants} potential attendees."
            ),
            expected_output=(
                "Report on marketing activities "
                "and attendee engagement formatted as markdown."
            ),
            output_file="marketing_report.md",
            agent=self._agents.marketing_communication_agent(),
        )
        self.logistics_task = Task(
            description=(
                "Coordinate catering and "
                "equipment for an event "
                "with {expected_participants} participants "
                "on {tentative_date}."
            ),
            expected_output=(
                "Confirmation of all logistics arrangements "
                "including catering and equipment setup."
            ),
            human_input=True,
            async_execution=True,
            agent=self._agents.logistic_manager_agent(),
        )

class JobApplication:
    def __init__(self, agents: Optional[object] = None) -> None:
        self._agents = JobAgents()

        self.research_task = Task(
            description=(
                "Analyze the job posting URL provided ({job_posting_url}) "
                "to extract key skills, experiences, and qualifications "
                "required. Use the tools to gather content and identify "
                "and categorize the requirements."
            ),
            expected_output=(
                "A structured list of job requirements, including necessary "
                "skills, qualifications, and experiences."
            ),
            agent=self._agents.resume_researcher_agent(),
            async_execution=True
        )

        self.profile_task = Task(
            description=(
                "Compile a detailed personal and professional profile "
                "using the GitHub ({github_url}) URLs,linkedin ({linkedin_url}) URLs,and personal write-up "
                "({personal_writeup}). Utilize tools to extract and "
                "synthesize information from these sources."
            ),
            expected_output=(
                "A comprehensive profile document that includes skills, "
                "project experiences, contributions, interests, and "
                "communication style."
            ),
            agent=self._agents.profiler_agent(),
            async_execution=True
        )

        self.resume_strategy_task = Task(
            description=(
                "Using the profile and job requirements obtained from "
                "previous tasks, tailor the resume to highlight the most "
                "relevant areas. Employ tools to adjust and enhance the "
                "resume content. Make sure this is the best resume even but "
                "don't make up any information. Update every section, "
                "inlcuding the initial summary, work experience, skills, "
                "and education. All to better reflrect the candidates "
                "abilities and how it matches the job posting."
            ),
            expected_output=(
                "An updated resume that effectively highlights the candidate's "
                "qualifications and experiences relevant to the job."
            ),
            output_file="tailored_resume.md",
            context=[self.research_task, self.profile_task],
            agent=self._agents.resume_strategist_agent()
        )

        self.interview_preparation_task = Task(
            description=(
                "Create a set of potential interview questions and talking "
                "points based on the tailored resume and job requirements. "
                "Utilize tools to generate relevant questions and discussion "
                "points. Make sure to use these question and talking points to "
                "help the candiadte highlight the main points of the resume "
                "and how it matches the job posting."
            ),
            expected_output=(
                "A document containing key questions and talking points "
                "that the candidate should prepare for the initial interview."
            ),
            output_file="interview_materials.md",
            context=[self.research_task, self.profile_task, self.resume_strategy_task],
            agent=self._agents.interview_preparation_agent()
        )