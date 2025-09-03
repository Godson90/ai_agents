# Agents.py
from __future__ import annotations
import os
from typing import Optional
from crewai import Agent, LLM
from crewai_tools import SerperDevTool, ScrapeWebsiteTool


class Agents:
    """Factory that builds shared LLM and returns role-specific Agents."""
    def __init__(
        self,
        model: str = None,
        temperature: float = 0.5,
        api_key: Optional[str] = None,
    ):
        # If gpt-4.1 isn’t available in your account, swap to "gpt-4o-mini".
        self.llm = LLM(
            model=model or os.getenv("OPENAI_MODEL", "gpt-4.1"),
            temperature=temperature,
            api_key=api_key or os.getenv("OPENAI_API_KEY"),

        )
        self.search_tool = SerperDevTool()
        self.scrape_website_tool = ScrapeWebsiteTool()

    def planner(self) -> Agent:
        return Agent(
            role="Content Planner",
            goal="Plan engaging and factually accurate content on {topic}.",
            backstory=(
                "You’re planning a blog article about {topic}. "
                "You gather trustworthy info, outline key sections, and surface data/sources "
                "so the audience can learn and make informed decisions. "
                "Your output guides the Content Writer."
            ),
            allow_delegation=False,
            verbose=False,
            llm=self.llm,
        )

    def writer(self) -> Agent:
        return Agent(
            role="Content Writer",
            goal="Write a clear, insightful article on {topic} using the planner’s outline.",
            backstory=(
                "You transform the planner’s outline and sources into a readable, SEO-friendly draft. "
                "You clearly separate opinion from fact and cite supporting info when relevant."
                "You provide working url links for refrences."
            ),
            allow_delegation=False,
            verbose=False,
            llm=self.llm,
        )

    def editor(self) -> Agent:
        return Agent(
            role="Editor",
            goal="Polish the draft for accuracy, clarity, tone, and style.",
            backstory=(
                "You fact-check, improve flow, ensure balanced viewpoints, and align with brand voice. "
                "You remove ambiguity and fix grammar and structure."
                "You make sure url links are working perfectly for refrences"
            ),
            allow_delegation=False,
            verbose=False,
            llm=self.llm,
        )

    def support_agent(self) -> Agent:
        return Agent(
            role="Senior Support Representative",
            goal= "Be the most friendly and helpful "
                "support representative in your team",
            backstory=(
                "You work at DefenStack (https://www.defenstack.com) and "
                " are now working on providing "
                "support to {customer}, a super important customer "
                " for your company."
                "You need to make sure that you provide the best support!"
                "Make sure to provide full complete answers, "
                " and make no assumptions."
            )
            ,
            allow_delegation=False,
            verbose=True,
            llm=self.llm,
        )

    def support_quality_assurance_agent(self) -> Agent:
        return Agent(
            role="Support Quality Assurance Specialist",
            goal= "Get recognition for providing the "
                "best support quality assurance in your team",
            backstory=(
                "on a request from {customer} ensuring that "
                "the support representative is "
                "providing the best support possible.\n"
                "You need to make sure that the support representative "
                "is providing full"
                "complete answers, and make no assumptions."
            ),
            verbose=False,
            llm=self.llm,
        )


    def sales_rep_agent(self) -> Agent:
        return Agent(
            role="Sales Representative",
            goal= "Identify high-value leads that match our ideal customer profile",
            backstory=(
                "As a part of the dynamic sales team at Defenstack, "
                "your mission is to scour "
                "the digital landscape for potential leads. "
                "Armed with cutting-edge tools "
                "and a strategic mindset, you analyze data, "
                "trends, and interactions to "
                "unearth opportunities that others might overlook. "
                "Your work is crucial in paving the way "
                "for meaningful engagements and driving the company's growth."
            ),
            allow_delegation=False,
            verbose=False,
            llm=self.llm
        )

    def lead_sales_rep_agent(self) -> Agent:
        return Agent(
            role="Lead Sales Representative",
            goal= "Nurture leads with personalized, compelling communications ",
            backstory=(
                "Within the vibrant ecosystem of Defenstack's sales department, "
                "you stand out as the bridge between potential clients "
                "and the solutions they need."
                "By creating engaging, personalized messages, "
                "you not only inform leads about our offerings "
                "but also make them feel seen and heard."
                "Your role is pivotal in converting interest "
                "into action, guiding leads through the journey "
                "from curiosity to commitment."
            ),
            allow_delegation=False,
            verbose=False,
            llm=self.llm
        )

    def venue_cordinator_agent(self) -> Agent:

        return Agent(
            role="Venue Cordinator",
            goal= "Identify and book an appropriate venue "
            "based on event requirements",
            backstory=(
                "With a keen sense of space and "
                "understanding of event logistics, "
                "you excel at finding and securing "
                "the perfect venue that fits the event's theme, "
                "size, and budget constraints."
            ),
            tools=[self.search_tool, self.scrape_website_tool],
            verbose=True,
            llm=self.llm,
        )

    def logistic_manager_agent(self) -> Agent:
        return Agent(
            role="Logistic Manager",
            goal= (
                "Manage all logistics for the event "
                "including catering and equipmen"
            ),
            backstory=(
                "Organized and detail-oriented, "
                "you ensure that every logistical aspect of the event "
                "from catering to equipment setup "
                "is flawlessly executed to create a seamless experience."
            ),
            tools=[self.search_tool, self.scrape_website_tool],
            verbose=True,
            llm=self.llm,
        )

    def marketing_communication_agent(self) -> Agent:
        return Agent(
            role="Marketing and Communication Agent",
            goal="Effectively market the event and "
                "communicate with participants",
            tools=[self.search_tool, self.scrape_website_tool],
            verbose=True,
            backstory=(
                "Creative and communicative, "
                "you craft compelling messages and "
                "engage with potential attendees "
                "to maximize event exposure and participation."
            ),
            llm=self.llm,
        )