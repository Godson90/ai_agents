# tasks.py
from __future__ import annotations
import warnings
from typing import List, Optional
from crewai import Task
from crewai_tools import  ScrapeWebsiteTool
from Agents import Agents


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
            description=(
                "1) Prioritize the latest trends, key players, and noteworthy news on {topic}.\n"
                "2) Identify the target audience and their interests/pain points.\n"
                "3) Develop a detailed content outline (intro, key points, call to action).\n"
                "4) Include SEO keywords and relevant data/sources (links if available)."
            ),
            expected_output=(
                "A comprehensive content plan with: outline, audience analysis, "
                "SEO keywords, and a sources list."
            ),
            agent=self._agents.planner(),
        )

        self.write_task: Task = Task(
            description=(
                "Using the content plan, draft a compelling blog post on {topic}.\n"
                "- Incorporate SEO keywords naturally.\n"
                "- Use clear section headings/subtitles.\n"
                "- Structure: engaging introduction, insightful body, crisp conclusion.\n"
                "- Proofread for grammar and brand voice alignment."
            ),
            expected_output=(
                "A well-written Markdown blog post, publication-ready. "
                "Each section should have 2–3 paragraphs."
            ),
            agent=self._agents.writer(),
            context=[self.plan_task],  # <-- reference the already-built plan_task
        )

        self.edit_task: Task = Task(
            description=(
                "Edit the draft for clarity, grammar, factual accuracy, and brand voice. "
                "Tighten phrasing and fix any structural issues."
            ),
            expected_output=(
                "A polished Markdown article, publication-ready; "
                "each section with 2–3 cohesive paragraphs."
            ),
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
            description=(
                    "{customer} just reached out with a super important ask:\n"
                    "{inquiry}\n\n"
                    "{person} from {customer} is the one that reached out. "
                    "Make sure to use everything you know "
                    "to provide the best support possible."
                    "You must strive to provide a complete "
                    "and accurate response to the customer's inquiry."
                    "No Hallucinations."
                ),
            expected_output=(
                    "A detailed, informative response to the "           
                    "customer's inquiry that addresses "
                    "all aspects of their question.\n"
                    "The response should include references "
                    "to everything you used to find the answer, "
                    "Excluding external data or solutions. "
                    "Ensure the answer is complete, "
                    "leaving no questions unanswered, and maintain a helpful and friendly "
                    "tone throughout."
                ),
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

