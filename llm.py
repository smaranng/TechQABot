import requests

def query_llm_with_ollama(prompt, model="tinyllama", min_tokens=50, max_tokens=200):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "min_tokens": min_tokens,
                    "max_tokens": max_tokens
                }
            }
        )
        response.raise_for_status()
        return response.json().get("response", "⚠️ No response from LLM.")
    except requests.exceptions.RequestException as e:
        return f"❌ LLM Error: {e}"
