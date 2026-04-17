class RRFService:
    def __init__(self, k: int = 60):
        self.k = k

    def combine(self, bm25_results, semantic_results):
        scores = {}

        def add(results):
            for rank, item in enumerate(results):
                pmid = item["article"].pmid
                scores[pmid] = scores.get(pmid, 0) + 1 / (self.k + rank + 1)

        add(bm25_results)
        add(semantic_results)

        article_map = {
            item["article"].pmid: item["article"]
            for item in bm25_results + semantic_results
        }

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        return [
            {"article": article_map[pmid], "score": score}
            for pmid, score in ranked
        ]
