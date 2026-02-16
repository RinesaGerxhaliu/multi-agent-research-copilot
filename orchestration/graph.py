from langgraph.graph import StateGraph, END
from shared_state import SharedState
from agents.planner_agent import PlannerAgent
from agents.research_agent import ResearchAgent
from agents.writer_agent import WriterAgent
from agents.verifier_agent import VerifierAgent

planner_agent = PlannerAgent()
research_agent = ResearchAgent()
writer_agent = WriterAgent()
verifier_agent = VerifierAgent()

def plan_node(state: SharedState) -> SharedState:
    return planner_agent.run(state)

def research_node(state: SharedState) -> SharedState:
    return research_agent.run(state)

def writer_node(state: SharedState) -> SharedState:
    return writer_agent.run(state)

def verifier_node(state: SharedState) -> SharedState:
    return verifier_agent.run(state)

def route_after_plan(state: SharedState):
    if not state.plan or state.plan == ["Not found in sources."]:
        return "verify"
    return "research"

def route_after_research(state: SharedState):
    if not state.research_notes:
        return "verify"
    return "write"

def build_graph():
    graph = StateGraph(SharedState)

    graph.add_node("plan", plan_node)
    graph.add_node("research", research_node)
    graph.add_node("write", writer_node)
    graph.add_node("verify", verifier_node)

    graph.set_entry_point("plan")

    graph.add_conditional_edges(
        "plan",
        route_after_plan,
        {
            "research": "research",
            "verify": "verify",
        },
    )

    graph.add_conditional_edges(
        "research",
        route_after_research,
        {
            "write": "write",
            "verify": "verify",
        },
    )

    graph.add_edge("write", "verify")
    graph.add_edge("verify", END)

    return graph.compile()
