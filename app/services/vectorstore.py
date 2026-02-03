import faiss
import numpy as np

# MiniLM embedding dimension
EMBEDDING_DIM = 384


class VectorStore:
    def __init__(self):
        self.index = faiss.IndexFlatL2(EMBEDDING_DIM)
        self.texts = []

    def add(self, embeddings, texts):
        embeddings = np.array(embeddings).astype("float32")
        self.index.add(embeddings)
        self.texts.extend(texts)

    def search(self, query_embedding, k=5):
        query_embedding = np.array([query_embedding]).astype("float32")
        _, indices = self.index.search(query_embedding, k)
        return [self.texts[i] for i in indices[0]]


# -----------------------------
# Global Vector Stores
# -----------------------------

job_vector_store = VectorStore()
resume_vector_store = VectorStore()
