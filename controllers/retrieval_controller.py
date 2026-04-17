from models.enums import RetrievalMethod


class RetrievalController:
    def __init__(self, bm25_service, semantic_service, rrf_service):
        self.bm25 = bm25_service
        self.semantic = semantic_service
        self.rrf = rrf_service

    def search(self, query, method: RetrievalMethod):
        if method == RetrievalMethod.BM25:
            return self.bm25.search(query)

        elif method == RetrievalMethod.SEMANTIC:
            return self.semantic.search(query)

        elif method == RetrievalMethod.HYBRID:
            bm25_res = self.bm25.search(query)
            sem_res = self.semantic.search(query)
            return self.rrf.combine(bm25_res, sem_res)