# agents/summarizer.py
# Summarizer agent that creates final report

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from prompts import SUMMARIZER_PROMPT, REFLECTION_PROMPT


class SummarizerAgent:
    """Agent that creates final reports"""

    def __init__(self, llm):
        """Initialize with a language model"""
        self.llm = llm

    def summarize(self, topic: str, notes: dict) -> str:
        """
        Create a final research report

        Args:
            topic: Research topic
            notes: Dictionary of section -> notes

        Returns:
            Final report as string
        """
        # Format notes
        notes_text = ""
        for section, content in notes.items():
            notes_text += f"\n=== {section} ===\n{content}\n"

        prompt = SUMMARIZER_PROMPT.format(
            topic=topic,
            notes=notes_text
        )

        messages = [
            SystemMessage(content="You are a professional report writer. Create comprehensive research reports."),
            HumanMessage(content=prompt)
        ]

        response = self.llm.invoke(messages)
        return response.content

    def reflect_and_improve(self, report: str) -> str:
        """
        Review and improve the report

        Args:
            report: Original report

        Returns:
            Improved report
        """
        prompt = REFLECTION_PROMPT.format(report=report)

        messages = [
            SystemMessage(content="You are a quality reviewer. Improve research reports."),
            HumanMessage(content=prompt)
        ]

        response = self.llm.invoke(messages)
        return response.content


def create_summarizer_agent():
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7
    )
    return SummarizerAgent(llm)