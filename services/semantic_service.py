import numpy as np
from sentence_transformers import SentenceTransformer


class SemanticService:
    def __init__(self, corpus, model_name: str):
        self.model = SentenceTransformer(model_name)
        self.documents = list(corpus.get_all())

        texts = [
            (doc.title + " " + (doc.abstract or ""))
            for doc in self.documents
        ]

        self.embeddings = self.model.encode(texts, normalize_embeddings=True)

    def search(self, query: str, top_k: int = 5):
        query_vec = self.model.encode(query, normalize_embeddings=True)

        scores = np.dot(self.embeddings, query_vec)

        ranked = sorted(
            zip(self.documents, scores),
            key=lambda x: x[1],
            reverse=True
        )

        return [
            {"article": doc, "score": float(score)}
            for doc, score in ranked[:top_k]
        ]
