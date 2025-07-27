from llm import query_llm_with_ollama

def generate_answer(user_query, docs):
    context = "\n\n".join([d['content'] for d in docs])
    prompt = f"User Question:\n{user_query}\n\nRelevant Context:\n{context}\n\nAnswer:"
    return query_llm_with_ollama(prompt)
