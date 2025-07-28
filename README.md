## 🧠 Tech QA Bot




🤖 Tech QA Bot is an intelligent QnA assistant built using Python, leveraging advanced Retrieval-Augmented Generation (RAG) techniques—including Plain RAG, Hybrid RAG, and Agentic RAG with LangGraph, powered by ChromaDB and TinyLLaMA (via Ollama). It provides answers from technical communities like Reddit and Stack Overflow, with a user-friendly Streamlit interface and API endpoints powered by FastAPI.

## 🚀 Features

- 🔍 **Plain RAG Pipeline** using ChromaDB for simple retrieval and generation.
- 🤖 **Hybrid RAG Pipeline** with validation, reranking, and improved answer quality.
- 🕸️ **Agentic RAG Pipeline** using LangGraph with multiple intelligent agents.
- 🌐 **Streamlit Interface** for an interactive chatbot and user-configurable parameters.
- ⚙️ **FastAPI Endpoints** for Plain, Hybrid, and Agentic RAG APIs.
- 💾 **SQLite Databases** to store scraped content and embeddings.
- 📥 **Reddit & Stack Overflow Scrapers** using PRAW and BeautifulSoup.
- 🔧 **Flask-based Web Interface** to view database records.

## 🛠 Tech Stack

| Component       | Technology                                      |
|-----------------|--------------------------------------------------|
| LLM             | TinyLLaMA via Ollama                             |
| Vector Store    | ChromaDB                                         |
| Agent Framework | LangGraph                                        |
| Embeddings      | Sentence Transformers (`all-MiniLM-L6-v2`)       |
| UI              | Streamlit, HTML, CSS                             |
| APIs            | FastAPI, Flask                                   |
| Scraping        | PRAW (Reddit), BeautifulSoup (Stack Overflow)    |
| Database        | SQLite (`techqa.db`, `stackoverflow.db`)         |



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
📁 agents/ — Modular Agents for Agentic RAG

| File                  | Description                                                         |
|-----------------------|---------------------------------------------------------------------|
| `qa_agent.py`         | Generates answers using the retrieved documents and LLM.            |
| `search_agent.py`     | Performs vector-based search using ChromaDB.                        |
| `similarity_agent.py` | Measures semantic similarity between query and documents.           |
| `validation_agent.py` | Validates the generated answer based on relevance and correctness.  |

---

📁 assets/ — UI Images

| File             | Description                                 |
|------------------|---------------------------------------------|
| `stack.png`      | Stack Overflow logo used in the UI.         |
| `reddit.png`     | Reddit logo used in the UI.                 |
| `techqa_logo.png`| Main branding/logo of Tech QA Bot.          |
| `logo.png`       | Alternative or additional branding image.   |

---

📁 chroma/ — ChromaDB Persistent Storage

| File             | Description                                                      |
|------------------|------------------------------------------------------------------|
| `chroma.sqlite3` | SQLite-based vector store used by ChromaDB for retrieval.        |

---

📁 database/ — Local Database Handler

| File     | Description                                                            |
|----------|------------------------------------------------------------------------|
| `db.py`  | Handles SQLite operations for inserting and managing scraped Q&A data. |

---

📁 pages/ — Streamlit Multi-Page Support

| File               | Description                                                                      |
|--------------------|----------------------------------------------------------------------------------|
| `Configuration.py` | A Streamlit UI page for setting configuration or parameters (e.g., model, mode). |

---

📁 scraping/ — Web Scraping Scripts

| File                | Description                                           |
|---------------------|-------------------------------------------------------|
| `reddit_scraper.py` | Scrapes tech Q&A posts from Reddit using PRAW.        |
| `so_scraper.py`     | Contains logic to scrape Stack Overflow HTML pages.   |
| `scraper_main_so.py`| Entry script to control Stack Overflow scraping flow. |

---

📁 utils/ — Utility Scripts

| File        | Description                                                   |
|-------------|---------------------------------------------------------------|
| `clean.py`  | Cleans HTML/text content from scraped posts before embedding. |

---

## 🔧 Core Scripts

| File                         | Description                                                             |
|------------------------------|-------------------------------------------------------------------------|
| `embeder_reddit.py`          | Embeds Reddit data into ChromaDB vector store.                          |
| `embedder_stackoverflow.py`  | Embeds Stack Overflow data into ChromaDB vector store.                  |
| `ChatBot.py`                 | Launches the main Streamlit chatbot UI.                                 |
| `viewdatabase.py`            | Flask app to view stored queries and answers in a simple web interface. |

---

## 🔌 API Endpoints — FastAPI Interfaces

| File                 | Description                                                        |
|----------------------|--------------------------------------------------------------------|
| `plain_rag_api.py`   | FastAPI backend for plain RAG: search + generate.                  |
| `hybrid_rag_api.py`  | FastAPI backend for hybrid RAG: search + validate + generate.      |
| `langgraph_api.py`   | FastAPI backend for agentic RAG using LangGraph.                   |

---

## 🔁 LangGraph-Based Agentic Pipeline

| File                   | Description                                                                |
|------------------------|----------------------------------------------------------------------------|
| `agentic_bot.py`       | Hybrid RAG controller integrating agents into a reasoning loop.            |
| `graph_builder.py`     | Builds the LangGraph DAG using nodes like search, QA, validate.            |
| `llm.py`               | Handles querying the TinyLLaMA model through Ollama.                       |
| `main_agentic_rag.py`  | Main script to orchestrate the full agentic pipeline using LangGraph.      |
| `nodes.py`             | Defines the logic for each node (agent) used in LangGraph.                 |
| `run_agentic_rag.py`   | Runs the LangGraph workflow locally for testing or inference.              |
| `search.py`            | Search logic used in plain and hybrid RAG workflows.                       |
| `state.py`             | Global state management for LangGraph workflows.                           |

---

## 🌐 Frontend & Styling

| File         | Description                                               |
|--------------|-----------------------------------------------------------|
| `index.html` | Landing page or static HTML (used optionally with Flask). |
| `style.css`  | CSS file for styling web UI components.                   |

---

## 📦 Misc

| File                | Description                                              |
|---------------------|----------------------------------------------------------|
| `requirements.txt`  | Python dependencies list.                                |
| `stackoverflow.db`  | SQLite database with scraped Stack Overflow data.        |
| `techqa.db`         | SQLite database with scraped Reddit data.                |

---

## ⚙ Installation

1. **Clone the Repository**
```

git clone https://github.com/smaranng/TechQABot.git
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
   
- Ollama download link:  https://ollama.com/download
- Ensure Ollama is installed and running.
```

ollama run tinyllama

```
## Please go through the notes before running the project.

## 🚦 How to Run the Components

Open multiple terminal tabs and run the following:

**Backend APIs:**

# Plain RAG API
```
uvicorn plain_rag_api:app --reload --port 8000
```
# LangGraph Agentic RAG API
```
uvicorn langgraph_api:app --reload --port 8001
```
# Hybrid RAG API
```
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
- Run the embedding scripts (`embedder_stackoverflow.py`, `embeder_reddit.py`) after scraping to populate ChromaDB.
- Assets like `stack.png`, `reddit.png`, and `techqa_logo.png` are used in the UI. *Do not remove them.*
- The system uses `stackoverflow.db` and `techqa.db` for storing forum content and scraped data.
- Make sure Ollama is installed and the TinyLLaMA model is available locally.
- The database viewer (Flask) uses index.html and style.css for a clean UI.

## 🙌 Credits

- **LLM**: [Ollama](https://ollama.com)
- **RAG Orchestration**: [LangGraph](https://www.langgraph.dev/)
- **Embeddings**: [SentenceTransformers](https://www.sbert.net/)
- **Vector DB**: [ChromaDB](https://www.trychroma.com/)









