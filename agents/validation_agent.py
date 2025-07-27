def is_valid_python_question(prompt: str) -> bool:
    python_keywords = ["python", "flask", "django", "numpy", "pandas", "tkinter", "list", "dict", "loop", "function", "class","keras","pytorch"]
    greetings = ["hi", "hello", "hey", "thanks", "thank you", "ok", "cool", "good morning", "good night", "yo"]

    prompt_lower = prompt.strip().lower()
    if any(greet in prompt_lower for greet in greetings) and len(prompt_lower.split()) <= 3:
        return True
    return any(keyword in prompt_lower for keyword in python_keywords)
