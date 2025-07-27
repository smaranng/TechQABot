from sentence_transformers import SentenceTransformer
from chromadb import PersistentClient
from llm import query_llm_with_ollama

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to persisted ChromaDB
chroma_client = PersistentClient(path="./chroma")
collection = chroma_client.get_or_create_collection("tech_qa")

print("📊 Total documents in ChromaDB collection:", collection.count())

def is_python_question(query):
    """Simple keyword-based Python filter."""
    keywords = ["python", "pandas", "numpy", "py", "jupyter", "flask", "django", "matplotlib","tensorflow","Enum","PyTorch","list","set","tuple","for","loops","itertools.groupby()","iterator"]
    return any(kw in query.lower() for kw in keywords)

def search_similar_questions(query, top_k=15, similarity_threshold=0.45, source_filter=None):
    embedding = model.encode(query).tolist()

    def filter_results(results):
        docs = results["documents"][0]
        metas = results["metadatas"][0]
        distances = results["distances"][0]
        filtered = []

        for doc, meta, dist in zip(docs, metas, distances):
            similarity = 1 - dist
            if similarity >= similarity_threshold:
                filtered.append((doc, meta))
        return filtered

    if not source_filter or source_filter.lower() == "all":
        reddit_results = collection.query(
            query_embeddings=[embedding],
            n_results=top_k,
            where={"source": "reddit"}
        )
        so_results = collection.query(
            query_embeddings=[embedding],
            n_results=top_k,
            where={"source": "stackoverflow"}
        )
        combined = filter_results(reddit_results) + filter_results(so_results)
        return combined
    else:
        results = collection.query(
            query_embeddings=[embedding],
            n_results=top_k,
            where={"source": source_filter.lower()}
        )
        return filter_results(results)

def build_prompt(query, context_results):
    context_text = "\n\n".join([doc for doc, _ in context_results])
    return f"User Question:\n{query}\n\nRelevant Context:\n{context_text}\n\nAnswer:"

def search_and_answer(query, source_filter=None, top_k=5, min_tokens=50, max_tokens=2000, similarity_threshold=0.45):
    if not is_python_question(query):
        return {
            "answer": "❌ I can only assist with **Python-related** questions. Please ask something about Python.",
            "source_docs": [],
            "source_ids": [],
            "source_urls": [],
            "source_scores": [],
            "is_accepted_flags": [],
            "source_tags": [],
            "source_platforms": []
        }

    results = search_similar_questions(query, top_k=top_k, similarity_threshold=similarity_threshold, source_filter=source_filter)

    if results:
        docs = []
        for _, meta in results:
            source = meta.get("source", "unknown")
            source_tag = "🟥 Reddit" if source == "reddit" else "🟦 StackOverflow"
            qa_text = f"{source_tag} Q: {meta['title']}\n\nA: {meta['answer']}"
            docs.append(qa_text)

        prompt = build_prompt(query, [(doc, {}) for doc in docs])
        llm_answer = query_llm_with_ollama(prompt, min_tokens=min_tokens, max_tokens=max_tokens)

        return {
            "answer": llm_answer,
            "source_docs": docs,
            "source_ids": [meta["question_id"] for _, meta in results],
            "source_urls": [meta.get("url", "") for _, meta in results],
            "source_scores": [meta.get("score", 0) for _, meta in results],
            "is_accepted_flags": [meta.get("is_accepted", False) for _, meta in results],
            "source_tags": [meta.get("source", "unknown") for _, meta in results],
            "source_platforms": [meta["source"] for _, meta in results]
        }
    else:
        llm_answer = query_llm_with_ollama(prompt, min_tokens=min_tokens, max_tokens=max_tokens)
        return {
            "answer": llm_answer,
            "source_docs": [],
            "source_ids": [],
            "source_urls": [],
            "source_scores": [],
            "is_accepted_flags": [],
            "source_tags": [],
            "source_platforms": []
        }

def get_general_reply(query):
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

    q = query.strip().lower()
    if len(q.split()) <= 3:
        return greetings.get(q)
    return None
# Debug/Test
if __name__ == "__main__":
    query = "Is Pytorch undoubtedly better than Keras?"
    print(f"\n🔍 Query: {query}")
    result = search_and_answer(query, source_filter="all", top_k=5)

    if result["source_docs"]:
        print(f"\n✅ Found {len(result['source_docs'])} matching Q&A(s):\n")
        for i, (doc, url, score, is_accepted) in enumerate(
            zip(result["source_docs"], result["source_urls"], result["source_scores"], result["is_accepted_flags"]), 1
        ):
            print(f"Result {i}:")
            print(doc[:300])
            print(f"🔗 URL: {url}")
            print(f"⭐ Score: {score} | ✅ Accepted: {bool(is_accepted)}")
            print("-" * 50)
    else:
        print("❌ No similar question found. LLM fallback used.\n")
        print(result["answer"])
