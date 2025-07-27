# nodes.py
from agents.validation_agent import is_valid_python_question
from agents.search_agent import get_relevant_docs
from agents.similarity_agent import compute_similarity
from agents.qa_agent import generate_answer
from llm import query_llm_with_ollama
from main_agentic_rag import get_general_reply

def validate_node(state):
    prompt = state["prompt"]
    if is_valid_python_question(prompt):
        return {"is_valid": True}
    else:
        general = get_general_reply(prompt)
        return {"is_valid": False, "general_response": general or "❌ Invalid query."}

def search_node(state):
    top_k = state.get("top_k", 5) 
    return {"docs": get_relevant_docs(state["prompt"], top_k=top_k)}

def similarity_node(state):
    scores = compute_similarity(state["prompt"], state["docs"])
    thresholded_docs = [doc for doc, score in zip(state["docs"], scores) if score >= 0.45]
    return {"sim_scores": scores, "thresholded_docs": thresholded_docs}

def answer_node(state):
    prompt = state["prompt"]
    docs = state.get("thresholded_docs", [])
    if not docs:
        return {"answer": query_llm_with_ollama(prompt)}
    return {"answer": generate_answer(prompt, docs)}
