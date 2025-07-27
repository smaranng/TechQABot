from agents.validation_agent import is_valid_python_question
from agents.search_agent import get_relevant_docs
from agents.qa_agent import generate_answer
from agents.similarity_agent import compute_similarity
from llm import query_llm_with_ollama

def get_general_reply(prompt):
    greetings = {
        "hi": "Hello! 👋 How can I help you today?",
        "hello": "Hi there! 😊 What would you like to ask?",
        "hey": "Hey! 👋 Need any help?",
        "yo": "Yo! 😎 What do you want to learn today?",
        "thanks": "You're welcome! 🙌",
        "thank you": "Glad to help! 😊",
        "ok": "Great! Let me know if you need anything else. 👍",
        "cool": "Awesome! 🎉 Need anything else?",
        "good morning": "Good morning! 🌞 How can I assist you?",
        "good night": "Good night! 😴 Let me know if you need help tomorrow."
    }
    return greetings.get(prompt.strip().lower())

def agentic_rag_pipeline(prompt):
    # Agent 1: Validate
    if not is_valid_python_question(prompt):
        general = get_general_reply(prompt)
        return {"answer": general or "❌ Invalid query. Ask something about Python.", "sources": []}

    # Agent 2: Search
    docs = get_relevant_docs(prompt)
    print("Retrieved docs:  ",docs)

    # Agent 3: Similarity Scoring
    sim_scores = compute_similarity(prompt, docs)
    thresholded_docs = [doc for doc, score in zip(docs, sim_scores) if score >= 0.45]

    if not thresholded_docs:
        answer = query_llm_with_ollama(prompt)
        return {"answer": answer, "sources": []}

    # Agent 4: Answer Generation
    answer = generate_answer(prompt, thresholded_docs)

    source_urls = [doc["meta"].get("url", "") for doc in thresholded_docs]
    
    return {"answer": answer, "sources": source_urls}

# FastAPI for qa_app.py integration
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"])

@app.get("/ask")
def ask(q: str):
    result = agentic_rag_pipeline(q)

    # Extract from metadata
    docs = get_relevant_docs(q)
    sim_scores = compute_similarity(q, docs)
    thresholded_docs = [doc for doc, score in zip(docs, sim_scores) if score >= 0.45]

    if not thresholded_docs:
        return JSONResponse(content={
            "answer": result["answer"],
            "source_urls": [],
            "source_scores": [],
            "is_accepted_flags": [],
            "source_platforms": []
        })

    return JSONResponse(content={
        "answer": result["answer"],
        "source_urls": [doc["meta"].get("url", "") for doc in thresholded_docs],
        "source_scores": [doc["meta"].get("score", 0) for doc in thresholded_docs],
        "is_accepted_flags": [doc["meta"].get("is_accepted", False) for doc in thresholded_docs],
        "source_platforms": [doc["meta"].get("source", "") for doc in thresholded_docs]
    })


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
