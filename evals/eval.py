from collections import defaultdict
from sentence_transformers import SentenceTransformer, util
from models.enums import RetrievalMethod


class Evaluator:
    def __init__(self, retriever, model_name):
        self.retriever = retriever
        self.model = SentenceTransformer(model_name)

        self.docs = retriever.bm25.documents

        self.doc_embeddings = self.model.encode(
            [
                "passage: " + (d.title + " " + (d.abstract or "")).lower()
                for d in self.docs
            ],
            normalize_embeddings=True
        )

        self.doc_id_map = {
            id(doc): i for i, doc in enumerate(self.docs)
        }

    def precision_at_k(self, results, query, k=5):
        if not results:
            return 0.0

        query_emb = self.model.encode(
            "query: " + query.lower(),
            normalize_embeddings=True
        )

        relevant = 0

        for r in results[:k]:
            doc = r["article"]

            idx = self.doc_id_map.get(id(doc))
            if idx is None:
                continue

            score = util.cos_sim(
                query_emb,
                self.doc_embeddings[idx]
            ).item()

            if score >= 0.45:
                relevant += 1

        return relevant / k

    def evaluate_query(self, query: str):
        bm25 = self.retriever.search(query, method=RetrievalMethod.BM25)
        semantic = self.retriever.search(query, method=RetrievalMethod.SEMANTIC)
        hybrid = self.retriever.search(query, method=RetrievalMethod.HYBRID)

        return {
            "query": query,
            "bm25_precision@5": self.precision_at_k(bm25, query),
            "semantic_precision@5": self.precision_at_k(semantic, query),
            "hybrid_precision@5": self.precision_at_k(hybrid, query),
        }

    def evaluate_all(self, queries):
        return [self.evaluate_query(q) for q in queries]
    def __init__(self, retriever, model_name):
        self.retriever = retriever
        self.model = SentenceTransformer(model_name)

        # Get documents from corpus (BM25 source)
        self.docs = retriever.bm25.documents

        # Precompute document embeddings once (for efficiency)
        texts = [
            "passage: " + (d.title + " " + (d.abstract or "")).lower()
            for d in self.docs
        ]

        self.doc_embeddings = self.model.encode(
            texts,
            normalize_embeddings=True
        )

    def _is_relevant(self, query: str, doc_index: int, threshold=0.45):
        """
        Compare query embedding vs precomputed doc embeddings.
        """
        query_emb = self.model.encode(
            "query: " + query.lower(),
            normalize_embeddings=True
        )

        score = util.cos_sim(
            query_emb,
            self.doc_embeddings[doc_index]
        ).item()

        return score >= threshold

    def precision_at_k(self, results, query, k=5):
        if not results:
            return 0.0

        top_k = results[:k]

        relevant = 0

        for r in top_k:
            doc = r["article"]

            # find index in corpus
            doc_index = self.docs.index(doc)

            if self._is_relevant(query, doc_index):
                relevant += 1

        return relevant / k

    def evaluate_query(self, query: str):
        """
        Evaluate all retrieval methods for a single query.
        """
        bm25 = self.retriever.search(query, method=RetrievalMethod.BM25)
        semantic = self.retriever.search(query, method=RetrievalMethod.SEMANTIC)
        hybrid = self.retriever.search(query, method=RetrievalMethod.HYBRID)

        return {
            "query": query,
            "bm25_precision@5": self.precision_at_k(bm25, query),
            "semantic_precision@5": self.precision_at_k(semantic, query),
            "hybrid_precision@5": self.precision_at_k(hybrid, query),
        }

    def evaluate_all(self, queries):
        """
        Run evaluation over multiple queries.
        """
        return [self.evaluate_query(q) for q in queries]