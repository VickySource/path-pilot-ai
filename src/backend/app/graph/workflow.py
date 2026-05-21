from langgraph.graph import END, StateGraph

from app.graph.edges import should_critique
from app.graph.nodes import (
    node_critique,
    node_extract_skills,
    node_gap_analysis,
    node_generate_roadmap,
    node_retrieve_context,
)
from app.graph.state import CareerState


def build_career_graph():
    graph = StateGraph(CareerState)
    graph.add_node("retrieve", node_retrieve_context)
    graph.add_node("extract", node_extract_skills)
    graph.add_node("gaps", node_gap_analysis)
    graph.add_node("roadmap", node_generate_roadmap)
    graph.add_node("critique", node_critique)

    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve", "extract")
    graph.add_edge("extract", "gaps")
    graph.add_edge("gaps", "roadmap")
    graph.add_conditional_edges("roadmap", should_critique, {"critique": "critique", "end": END})
    graph.add_edge("critique", END)

    return graph.compile()


_career_graph = build_career_graph()


async def run_career_workflow(goal: str, document_id: str | None = None) -> dict:
    initial: CareerState = {"goal": goal, "document_id": document_id}
    result = await _career_graph.ainvoke(initial)
    return dict(result)
