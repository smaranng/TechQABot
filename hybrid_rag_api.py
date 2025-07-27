from typing import Optional
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from search import search_and_answer, get_general_reply  
from agentic_bot import enhanced_search_and_answer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ask")
async def ask(request: Request, q: str, source: str = "all", top_k: int = 5): 
    # Check for general replies first
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

    # ✅ Pass source to search_and_answer
    result = search_and_answer(q, source_filter=source, top_k=top_k)
    return result

@app.get("/agent-bot")
def agent_bot(q: str, source: Optional[str] = None, top_k: int = 5, min_tokens: int = 50, max_tokens: int = 2000):
     return enhanced_search_and_answer(q, source=source, top_k=top_k, min_tokens=min_tokens, max_tokens=max_tokens)

