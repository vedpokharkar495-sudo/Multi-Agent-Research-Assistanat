# agents/planner.py
# Planner agent that creates research plans

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from prompts import PLANNER_PROMPT


class PlannerAgent:
    """Agent that creates a research plan"""

    def __init__(self, llm):
        """Initialize with a language model"""
        self.llm = llm

    def create_plan(self, topic: str) -> list:
        """
        Create a research plan for a topic

        Args:
            topic: Research topic

        Returns:
            List of research sections
        """
        prompt = PLANNER_PROMPT.format(topic=topic)

        messages = [
            SystemMessage(content="You are a research planner. Create structured research plans."),
            HumanMessage(content=prompt)
        ]

        response = self.llm.invoke(messages)

        # Parse the response into a list
        plan_text = response.content
        sections = []

        for line in plan_text.strip().split('\n'):
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-')):
                # Remove number/bullet and clean
                if line[0].isdigit():
                    section = line.split('.', 1)[-1].strip()
                else:
                    section = line[1:].strip()
                sections.append(section)

        # If parsing failed, use the whole text as one section
        if not sections:
            sections = [plan_text]

        return sections


# Create a singleton instance
def create_planner_agent():
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7
    )
    return PlannerAgent(llm)