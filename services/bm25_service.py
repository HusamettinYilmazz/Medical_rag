from rank_bm25 import BM25Okapi


class BM25Service:
    def __init__(self, corpus):
        self.documents = corpus.get_all()

        self.tokenized_docs = [
            (doc.title + " " + (doc.abstract or "")).lower().split()
            for doc in self.documents
        ]

        self.bm25 = BM25Okapi(self.tokenized_docs)

    def search(self, query: str, top_k: int = 5):
        query_tokens = query.lower().split()

        scores = self.bm25.get_scores(query_tokens)

        ranked = sorted(
            zip(self.documents, scores),
            key=lambda x: x[1],
            reverse=True
        )

        return [
            {"article": doc, "score": float(score)}
            for doc, score in ranked[:top_k]
        ]
