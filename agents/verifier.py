# agents/verifier.py
# Verification agent that checks research completeness

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from prompts import VERIFIER_PROMPT


class VerifierAgent:
    """Agent that verifies research completeness"""

    def __init__(self, llm):
        """Initialize with a language model"""
        self.llm = llm

    def verify(self, topic: str, notes: dict) -> tuple:
        """
        Verify if research is complete

        Args:
            topic: Research topic
            notes: Dictionary of section -> notes

        Returns:
            Tuple of (is_complete, missing_info, is_reliable)
        """
        # Format notes for prompt
        notes_text = ""
        for section, content in notes.items():
            notes_text += f"\n=== {section} ===\n{content}\n"

        prompt = VERIFIER_PROMPT.format(
            topic=topic,
            notes=notes_text
        )

        messages = [
            SystemMessage(content="You are a verification agent. Check research quality and completeness."),
            HumanMessage(content=prompt)
        ]

        response = self.llm.invoke(messages)
        response_text = response.content

        # Parse response
        is_complete = "COMPLETE: Yes" in response_text
        is_reliable = "RELIABLE: Yes" in response_text

        # Extract missing info
        missing_info = []
        if "MISSING:" in response_text:
            missing_part = response_text.split("MISSING:")[1].split("RELIABLE:")[0].strip()
            if missing_part and missing_part.lower() != "none":
                missing_info = [item.strip() for item in missing_part.split('\n') if item.strip()]

        return is_complete, missing_info, is_reliable


def create_verifier_agent():
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.3  # Lower temperature for consistency
    )
    return VerifierAgent(llm)