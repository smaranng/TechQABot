from sentence_transformers import util, SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def compute_similarity(query, docs):
    query_vec = model.encode(query, convert_to_tensor=True)
    doc_texts = [doc.get('text') or doc.get('content', '') for doc in docs]
    doc_vecs = model.encode(doc_texts, convert_to_tensor=True)

    similarities = util.pytorch_cos_sim(query_vec, doc_vecs)[0]
    return [float(score) for score in similarities]
