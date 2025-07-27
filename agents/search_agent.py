from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
client = PersistentClient(path="./chroma")
collection = client.get_or_create_collection("tech_qa")

def get_relevant_docs(prompt, top_k=5):
    query_results = collection.query(
        query_texts=[prompt],
        n_results=top_k,
        include=["documents", "metadatas"]  # Include metadata
    )

    docs = []
    for doc, meta in zip(query_results["documents"][0], query_results["metadatas"][0]):
        docs.append({"content": doc, "meta": meta})  # Attach metadata
    return docs
