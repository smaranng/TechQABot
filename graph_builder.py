# graph_builder.py
from langgraph.graph import StateGraph, END
from state import AgentState
from nodes import validate_node, search_node, similarity_node, answer_node

def build_rag_graph():
    graph = StateGraph(AgentState)

    graph.add_node("validate", validate_node)
    graph.add_node("search", search_node)
    graph.add_node("similarity", similarity_node)
    graph.add_node("answer", answer_node)

    # Branching logic
    def route_validation(state):
        return "answer" if not state.get("is_valid", False) else "search"

    graph.set_entry_point("validate")
    graph.add_conditional_edges("validate", route_validation, {
        "search": "search",
        "answer": "answer"  # General response if invalid
    })
    
    graph.add_edge("search", "similarity")
    graph.add_edge("similarity", "answer")
    graph.set_finish_point("answer")

    return graph.compile()
