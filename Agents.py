# Agents.py
from __future__ import annotations
import os
import yaml
from typing import Optional
from crewai import Agent, LLM
from config import config
from crewai_tools import SerperDevTool, ScrapeWebsiteTool,FileReadTool,MDXSearchTool


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
        self.read_resume = FileReadTool(file_path="./resume.md")
        #self.semantic_search_resume = MDXSearchTool(mdx="resume.md")

    def planner(self) -> Agent:
        return Agent(
            config=config()['article_planner_agent'],
            llm=self.llm,
        )

    def writer(self) -> Agent:
        return Agent(
            config= config()['writer_agent'],
            llm=self.llm,
        )

    def editor(self) -> Agent:
        return Agent(
            config= config()['editor_agent'],
            llm=self.llm,
        )

    def support_agent(self) -> Agent:
        return Agent(
            config=config()['support_agent'],
            llm=self.llm,
        )

    def support_quality_assurance_agent(self) -> Agent:
        return Agent(
            config=config()['support_quality_assurance_agent'],
            llm=self.llm,
        )


    def sales_rep_agent(self) -> Agent:
        return Agent(
            config=config()['sales_rep_agent'],
            llm=self.llm
        )

    def lead_sales_rep_agent(self) -> Agent:
        return Agent(
            config=config()['lead_sales_rep_agent'],
            llm=self.llm
        )

    def venue_cordinator_agent(self) -> Agent:

        return Agent(
            config=config()['venue_coordinator_agent'],
            tools=[self.search_tool, self.scrape_website_tool],
            llm=self.llm,
        )

    def logistic_manager_agent(self) -> Agent:
        return Agent(
            config=config()['logistic_manager_agent'],
            tools=[self.search_tool, self.scrape_website_tool],
            llm=self.llm,
        )

    def marketing_communication_agent(self) -> Agent:
        return Agent(
            config=config()['marketing_communication_agent'],
            tools=[self.search_tool, self.scrape_website_tool],
            llm=self.llm,
        )

class JobAgents:
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
        self.read_resume = FileReadTool(file_path="./resume.md")
        self.semantic_search_resume = MDXSearchTool(mdx="resume.md")


    def resume_researcher_agent(self) -> Agent:
        return Agent(
            config=config()['resume_research_agent'],
            tools=[self.scrape_website_tool, self.search_tool],
            verbose=True,
            llm=self.llm,
        )

    def profiler_agent(self) -> Agent:
        return Agent(
            config=config()['profiler_agent'],
            tools=[self.scrape_website_tool, self.search_tool,
                   self.read_resume, self.semantic_search_resume],
            verbose=True,
            llm=self.llm,
        )

    def resume_strategist_agent(self) -> Agent:
        return Agent(
            config=config()['resume_strategist_agent'],
            tools=[self.scrape_website_tool, self.search_tool,
                   self.read_resume, self.semantic_search_resume],
            verbose=True,
            llm=self.llm,
        )

    def interview_preparation_agent(self) -> Agent:
        return Agent(
            config=config()['interview_prep_agent'],
            tools=[self.scrape_website_tool, self.search_tool,
                   self.read_resume, self.semantic_search_resume],
            verbose=True,
            llm=self.llm,
        )