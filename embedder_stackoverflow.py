# embedder_stackoverflow.py

import sqlite3
from sentence_transformers import SentenceTransformer
from chromadb import PersistentClient

model = SentenceTransformer("all-MiniLM-L6-v2")
chroma_client = PersistentClient(path="./chroma")
collection = chroma_client.get_or_create_collection("tech_qa")

conn = sqlite3.connect("stackoverflow.db")
cursor = conn.cursor()

cursor.execute("""
    SELECT q.question_id, q.title, q.body, q.tags, a.body, a.score, a.is_accepted 
    FROM questions q 
    JOIN answers a ON q.question_id = a.question_id
    WHERE a.is_accepted = 1
""")

rows = cursor.fetchall()

for qid, q_title, q_body, tags, a_body, score, is_accepted in rows:
    embedding = model.encode(q_title).tolist()

    collection.add(
        documents=[q_title],
        metadatas=[{
            "question_id": qid,
            "title": q_title,
            "body": q_body,
            "tags": tags,
            "answer": a_body,
            "score": score,
            "is_accepted": is_accepted,
            "source": "stackoverflow",
            "url": f"https://stackoverflow.com/q/{qid}"
        }],
        ids=[f"so_{qid}_{score}"],
        embeddings=[embedding]
    )

conn.close()
print("✅ StackOverflow Q&A embedded using only question titles.")
