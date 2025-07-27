
# 🧠 Tech QA Bot
```

Tech QA Bot is an intelligent Q&A assistant built using Python, leveraging advanced Retrieval-Augmented Generation (RAG) techniques—including Plain RAG, Hybrid RAG, and Agentic RAG with LangGraph—powered by ChromaDB and TinyLLaMA (via Ollama). It provides answers from technical forums like Reddit and Stack Overflow, with a user-friendly Streamlit interface and API endpoints powered by FastAPI.
```
## 🚀 Features

- **Plain RAG pipeline** using ChromaDB for semantic search.
- **Hybrid RAG pipeline** with answer validation and reranking.
- **LangGraph-powered Agentic RAG** using multiple specialized agents.
- **Streamlit UI** for interactive chat.
- **FastAPI endpoints** for integrating different RAG pipelines.
- **SQLite backend** for storing scraped and embedded data.
- **Scraping logic** for Reddit and Stack Overflow tech Q&A.

## 🛠 Tech Stack

| Component     | Technology                                   |
|---------------|----------------------------------------------|
| LLM           | TinyLLaMA via Ollama                         |
| Vector Store  | ChromaDB                                     |
| Orchestration | LangGraph                                    |
| Web UI        | Streamlit                                    |
| API Framework | FastAPI                                      |
| Scraping      | PRAW (Reddit), BeautifulSoup (Stack Overflow)|
| Embedding     | Sentence Transformers                        |



## 📂 Project Structure

```
tech_qa_bot/
├── agents/
│   ├── qa_agent.py
│   ├── search_agent.py
│   ├── similarity_agent.py
│   └── validation_agent.py
├── assets/
│   ├── stack.png
│   ├── reddit.png
│   ├── techqa_logo.png
│   └── logo.png
├── chroma/
│   └── chroma.sqlite3
├── database/
│   └── db.py
├── pages/
│   └── Configuration.py
├── scraping/
│   ├── reddit_scraper.py
│   ├── so_scraper.py
│   └── scraper_main_so.py
├── utils/
│   └── clean.py
├── embeder_reddit.py
├── embedder_stackoverflow.py
├── ChatBot.py
├── hybrid_rag_api.py
├── langgraph_api.py
├── plain_rag_api.py
├── viewdatabase.py
├── agentic_bot.py
├── graph_builder.py
├── llm.py
├── main_agentic_rag.py
├── nodes.py
├── run_agentic_rag.py
├── search.py
├── state.py
├── index.html
├── style.css
├── requirements.txt
├── stackoverflow.db
└── techqa.db

```

## ⚙ Installation

1. **Clone the Repository**
```

git clone https://github.com/yourusername/tech_qa_bot.git
cd tech_qa_bot

```

2. **Create a Virtual Environment**
```

python -m venv venv
source venv/bin/activate  \# On Windows: venv\Scripts\activate

```

3. **Install Dependencies**
```

pip install -r requirements.txt

```

4. **Run Ollama and Load the Model**
- Ensure Ollama is installed and running.
```

ollama run tinyllama

```

## 🚦 How to Run the Components

Open multiple terminal tabs and run the following:

**Backend APIs:**
```
# Plain RAG API

uvicorn plain_rag_api:app --reload --port 8000

# LangGraph Agentic RAG API

uvicorn langgraph_api:app --reload --port 8001

# Hybrid RAG API

uvicorn hybrid_rag_api:app --reload --port 8002

```

**Streamlit UI:**
```
streamlit run ChatBot.py

```

**Database Viewer (optional):**
```

python viewdatabase.py

```

## 📌 Notes
```
- Run the embedding scripts (`embedder_stackoverflow.py`, `embeder_reddit.py`) after scraping to populate ChromaDB.
- Assets like `stack.png`, `reddit.png`, and `techqa_logo.png` are used in the UI. *Do not remove them.*
- The system uses `stackoverflow.db` and `techqa.db` for storing forum content and scraped data.
```


