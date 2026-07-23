# agents/researcher.py
# Research agent that gathers information

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from prompts import RESEARCH_PROMPT
from tools.search_tool import search_tool
from tools.rag_tool import rag_tool


class ResearchAgent:
    """Agent that researches specific sections"""

    def __init__(self, llm):
        """Initialize with a language model"""
        self.llm = llm

    def research_section(self, topic: str, section: str) -> str:
        """
        Research a specific section of the topic

        Args:
            topic: Main research topic
            section: Section to research

        Returns:
            Research notes as string
        """
        # Search the web
        search_query = f"{topic} {section}"
        search_results = search_tool.search(search_query, max_results=3)

        # Format search results
        search_text = ""
        for i, result in enumerate(search_results, 1):
            search_text += f"\nSource {i}: {result['title']}\n"
            search_text += f"Content: {result['content'][:500]}\n"
            search_text += f"URL: {result['url']}\n"

        # Retrieve from RAG
        rag_query = f"{topic} {section}"
        docs = rag_tool.retrieve(rag_query, k=2)
        doc_text = "\n".join([f"Document {i + 1}: {doc}" for i, doc in enumerate(docs)])

        # Generate research notes
        prompt = RESEARCH_PROMPT.format(
            topic=topic,
            section=section,
            documents=doc_text if doc_text else "No relevant documents found.",
            search_results=search_text if search_text else "No search results found."
        )

        messages = [
            SystemMessage(content="You are a research assistant. Gather comprehensive information."),
            HumanMessage(content=prompt)
        ]

        response = self.llm.invoke(messages)
        return response.content

    def research_all_sections(self, topic: str, plan: list) -> dict:
        """
        Research all sections in the plan

        Args:
            topic: Main research topic
            plan: List of sections to research

        Returns:
            Dictionary of section -> notes
        """
        notes = {}
        for section in plan:
            print(f"Researching: {section}")
            notes[section] = self.research_section(topic, section)
        return notes


def create_researcher_agent():
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7
    )
    return ResearchAgent(llm)