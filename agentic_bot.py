from sentence_transformers import SentenceTransformer
from chromadb import PersistentClient
from llm import query_llm_with_ollama

# Load model and DB
model = SentenceTransformer("all-MiniLM-L6-v2")
chroma_client = PersistentClient(path="./chroma")
collection = chroma_client.get_or_create_collection("tech_qa")


def is_valid_query(query):
    return len(query.strip().split()) > 3


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


def extract_tags_from_query(query):
    return [word.lower() for word in query.split() if len(word) > 3]


def narrow_semantic_search(query, top_k=5, similarity_threshold=0.45):
    embedding = model.encode(query).tolist()
    tags = extract_tags_from_query(query)

    tag_filters = {"$or": [{"tags": {"$contains": tag}} for tag in tags]}

    print("🧠 Semantic Search Tags:", tags)

    results = collection.query(
        query_embeddings=[embedding],
        n_results=top_k,
        where=tag_filters
    )

    filtered = []
    for doc, meta, dist in zip(results["documents"][0], results["metadatas"][0], results["distances"][0]):
        similarity = 1 - dist
        print(f"🔍 Doc Similarity: {similarity:.2f}")
        if similarity >= similarity_threshold:
            filtered.append((doc, meta))
    return filtered


def build_prompt(query, context_results, max_context_chars=1200):
    context_text = ""
    char_count = 0

    for doc, _ in context_results:
        if char_count + len(doc) > max_context_chars:
            break
        context_text += doc + "\n\n"
        char_count += len(doc)

    prompt = f"""You are a Python expert AI assistant helping users with technical questions.

User Question:
{query}

Relevant Context:
{context_text}

Answer:"""
    return prompt


def enhanced_search_and_answer(query, source=None, top_k=5, min_tokens=50, max_tokens=2000):
    print("📝 Received Query:", query)

    if not is_valid_query(query):
        general = get_general_reply(query)
        if general:
            print("💬 General reply triggered.")
            return {
                "answer": general,
                "source_docs": [],
                "source_ids": [],
                "source_urls": [],
                "source_scores": [],
                "is_accepted_flags": [],
                "source_tags": [],
                "source_platforms": []
            }

        print("🔁 Falling back to plain LLM due to short query.")
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

    results = narrow_semantic_search(query, top_k=top_k)

    if results:
        print(f"✅ {len(results)} relevant results found.")
        docs = []
        source_ids = []
        source_urls = []
        source_scores = []
        is_accepted_flags = []
        source_tags = []
        source_platforms = []

        for _, meta in results:
            source = meta.get("source", "unknown")
            source_tag = "🟥 Reddit" if source == "reddit" else "🟦 StackOverflow"
            qa_text = f"{source_tag} Q: {meta.get('title', '')[:150]}\n\nA: {meta.get('answer', '')[:500]}"
            docs.append(qa_text)

            source_ids.append(meta.get("question_id", ""))
            source_urls.append(meta.get("url", ""))
            source_scores.append(meta.get("score", 0))
            is_accepted_flags.append(meta.get("is_accepted", False))
            source_tags.append(source)
            source_platforms.append(source)

        prompt = build_prompt(query, [(doc, {}) for doc in docs])
        print("📤 Prompt sent to LLM (first 500 chars):")
        print(prompt[:500])

        llm_answer = query_llm_with_ollama(query, min_tokens=min_tokens, max_tokens=max_tokens)
        return {
            "answer": llm_answer,
            "source_docs": docs,
            "source_ids": source_ids,
            "source_urls": source_urls,
            "source_scores": source_scores,
            "is_accepted_flags": is_accepted_flags,
            "source_tags": source_tags,
            "source_platforms": source_platforms
        }

    print("❌ No context found. Falling back to plain LLM.")
    llm_answer = query_llm_with_ollama(query, min_tokens=min_tokens, max_tokens=max_tokens)
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