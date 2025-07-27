# embedder_reddit.py

import sqlite3
from sentence_transformers import SentenceTransformer
from chromadb import PersistentClient

model = SentenceTransformer("all-MiniLM-L6-v2")
client = PersistentClient(path="./chroma")
collection = client.get_or_create_collection("tech_qa")

conn = sqlite3.connect("techqa.db")
cursor = conn.cursor()

cursor.execute("SELECT question_id, title, body FROM questions_reddit")
questions = cursor.fetchall()

for qid, title, body in questions:
    cursor.execute(
        "SELECT body, score FROM answers_reddit WHERE question_id = ?", (qid,)
    )
    answers = cursor.fetchall()

    for ans_body, score in answers:
        embedding = model.encode(title).tolist()  # ✅ Only title is embedded

        metadata = {
            "question_id": qid,
            "title": title or "",
            "body": body or "",
            "answer": ans_body or "",
            "score": score if score is not None else 0,
            "is_accepted": "unknown",  # Reddit doesn't have this; keep as None
            "source": "reddit",
            "url": f"https://www.reddit.com/comments/{qid}"
        }

        doc_id = f"reddit_{qid}_{hash(ans_body)}"
        collection.add(
            ids=[doc_id],
            documents=[title],  # Only question for semantic search
            embeddings=[embedding],
            metadatas=[metadata]
        )

conn.close()
print("✅ Reddit Q&A embedded using only question titles.")