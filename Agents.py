# Agents.py
from __future__ import annotations
import os
from typing import Optional
from crewai import Agent, LLM
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
            ),
            allow_delegation=False,
            verbose=False,
            llm=self.llm,
        )