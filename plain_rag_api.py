from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from search import search_and_answer, get_general_reply  

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ask")
async def ask(
    request: Request,
    q: str,
    source: str = "all",
    top_k: int = 5,
    min_tokens: int = 50,
    max_tokens: int = 2000,
    threshold: float = 0.45  
):
    general = get_general_reply(q)
    if general:
        return {
            "answer": general,
            "source_docs": [],
            "source_ids": [],
            "source_urls": [],
            "source_scores": [],
            "is_accepted_flags": [],
            "source_tags": [],
            "source_platforms": [],
        }

    # ✅ Pass top_k to search_and_answer
    result = search_and_answer(q, source_filter=source, top_k=top_k, min_tokens=min_tokens, max_tokens=max_tokens, similarity_threshold=threshold)
    return result
