
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from run_agentic_rag import run_agentic_rag
from agents.search_agent import get_relevant_docs
from agents.similarity_agent import compute_similarity

app = FastAPI()

# CORS middleware for frontend to call this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ask")
async def ask(q: str, source: str = "all", top_k: int = 5, threshold: float = 0.45):
    result = run_agentic_rag(q, top_k=top_k, similarity_threshold=threshold)
    docs = get_relevant_docs(q, top_k=top_k)

    # Filter by platform if not "all"
    if source != "all":
        docs = [doc for doc in docs if doc["meta"].get("source", "") == source.lower()]

    sim_scores = compute_similarity(q, docs)
    thresholded_docs = [doc for doc, score in zip(docs, sim_scores) if score >= 0.45]

    if not thresholded_docs:
        return JSONResponse(content={
            "answer": result.get("answer", "No answer."),
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
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
