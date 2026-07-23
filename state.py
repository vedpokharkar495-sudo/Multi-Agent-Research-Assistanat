# state.py
# This defines the state that flows through our graph

from typing import List, Dict, Optional, TypedDict


class ResearchState(TypedDict):
    """State of our research assistant"""

    # Input
    topic: str  # Research topic from user

    # Planning
    plan: List[str]  # List of research sections

    # Research results
    search_results: List[Dict]  # Results from web search
    retrieved_docs: List[str]  # Documents from RAG

    # Notes and verification
    notes: Dict[str, str]  # Section name -> notes
    is_verified: bool  # Whether info is verified
    missing_info: List[str]  # What's missing

    # Final output
    final_summary: str  # Final report
    iterations: int  # Number of research iterations


def create_initial_state(topic: str) -> ResearchState:
    """Create initial state for a research topic"""
    return {
        "topic": topic,
        "plan": [],
        "search_results": [],
        "retrieved_docs": [],
        "notes": {},
        "is_verified": False,
        "missing_info": [],
        "final_summary": "",
        "iterations": 0
    }