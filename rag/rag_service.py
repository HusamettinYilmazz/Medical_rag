from rag.prompt_builder import build_prompt


class RAGService:
    def __init__(self, retriever, llm_service):
        self.retriever = retriever
        self.llm = llm_service

    def answer(self, query: str, method):
        # 1. retrieve
        docs = self.retriever.search(query, method)

        # 2. build prompt
        prompt = build_prompt(query, docs)

        # 3. generate
        answer = self.llm.generate(prompt)

        return {
            "query": query,
            "retrieved_docs": docs,
            "answer": answer
        }
