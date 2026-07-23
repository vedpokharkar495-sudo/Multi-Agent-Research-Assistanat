# graph.py
# This builds the LangGraph workflow

from typing import Literal
from langgraph.graph import StateGraph, END
from langgraph.checkpoint import MemorySaver
from langchain_openai import ChatOpenAI

from state import ResearchState
from agents.planner import PlannerAgent, create_planner_agent
from agents.researcher import ResearchAgent, create_researcher_agent
from agents.verifier import VerifierAgent, create_verifier_agent
from agents.summarizer import SummarizerAgent, create_summarizer_agent


class ResearchAssistant:
    """Main research assistant using LangGraph workflow"""

    def __init__(self):
        """Initialize the research assistant with all agents"""
        # Create LLM
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7
        )

        # Create agents
        self.planner = PlannerAgent(self.llm)
        self.researcher = ResearchAgent(self.llm)
        self.verifier = VerifierAgent(self.llm)
        self.summarizer = SummarizerAgent(self.llm)

        # Build the graph
        self.workflow = self._build_workflow()
        self.memory = MemorySaver()
        self.app = self.workflow.compile(checkpointer=self.memory)

    def _build_workflow(self):
        """Build the LangGraph workflow"""
        workflow = StateGraph(ResearchState)

        # Add nodes
        workflow.add_node("planner", self._plan_node)
        workflow.add_node("researcher", self._research_node)
        workflow.add_node("verifier", self._verify_node)
        workflow.add_node("summarizer", self._summary_node)

        # Add edges
        workflow.set_entry_point("planner")
        workflow.add_edge("planner", "researcher")
        workflow.add_edge("researcher", "verifier")

        # Conditional edge from verifier
        workflow.add_conditional_edges(
            "verifier",
            self._decide_next,
            {
                "continue_research": "researcher",
                "finish": "summarizer"
            }
        )

        workflow.add_edge("summarizer", END)

        return workflow

    def _plan_node(self, state: ResearchState) -> dict:
        """Plan node - creates research plan"""
        print("Planning research...")
        plan = self.planner.create_plan(state["topic"])
        return {"plan": plan}

    def _research_node(self, state: ResearchState) -> dict:
        """Research node - researches all sections"""
        print("Researching...")

        # Get plan
        plan = state.get("plan", [])
        if not plan:
            # If no plan, create one
            plan = self.planner.create_plan(state["topic"])
            state["plan"] = plan

        # Research all sections
        notes = self.researcher.research_all_sections(state["topic"], plan)

        # Update iterations
        iterations = state.get("iterations", 0) + 1

        return {"notes": notes, "iterations": iterations}

    def _verify_node(self, state: ResearchState) -> dict:
        """Verify node - checks if research is complete"""
        print("Verifying research...")

        is_complete, missing_info, is_reliable = self.verifier.verify(
            state["topic"],
            state.get("notes", {})
        )

        return {
            "is_verified": is_complete and is_reliable,
            "missing_info": missing_info
        }

    def _summary_node(self, state: ResearchState) -> dict:
        """Summary node - generates final report"""
        print("Generating report...")

        # Generate summary
        summary = self.summarizer.summarize(
            state["topic"],
            state.get("notes", {})
        )

        # Improve with reflection
        improved_summary = self.summarizer.reflect_and_improve(summary)

        return {"final_summary": improved_summary}

    def _decide_next(self, state: ResearchState) -> Literal["continue_research", "finish"]:
        """Decide whether to continue research or finish"""
        is_verified = state.get("is_verified", False)
        iterations = state.get("iterations", 0)
        missing_info = state.get("missing_info", [])

        # If not verified and haven't tried too many times, continue
        if not is_verified and iterations < 3 and missing_info:
            print(f"Missing information: {missing_info}")
            return "continue_research"
        else:
            if iterations >= 3:
                print("Max iterations reached. Generating report with available information.")
            return "finish"

    def research(self, topic: str) -> dict:
        """
        Run the research assistant on a topic

        Args:
            topic: Research topic

        Returns:
            Dictionary with results
        """
        from state import create_initial_state

        # Create initial state
        initial_state = create_initial_state(topic)

        # Run the workflow
        config = {"configurable": {"thread_id": "research_thread"}}
        final_state = self.app.invoke(initial_state, config)

        return {
            "topic": topic,
            "plan": final_state.get("plan", []),
            "notes": final_state.get("notes", {}),
            "report": final_state.get("final_summary", ""),
            "iterations": final_state.get("iterations", 0),
            "is_verified": final_state.get("is_verified", False)
        }


# Create a singleton instance
research_assistant = ResearchAssistant()