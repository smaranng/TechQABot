# run_agentic_rag.py
from graph_builder import build_rag_graph

rag_graph = build_rag_graph()

def run_agentic_rag(prompt: str, top_k: int = 5, similarity_threshold: float = 0.45):
    final_state = rag_graph.invoke({
        "prompt": prompt,
        "top_k": top_k,
        "similarity_threshold": similarity_threshold 
    })
    return final_state
