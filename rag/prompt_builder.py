def build_prompt(query: str, retrieved_docs):
    context = "\n\n".join([
        f"Title: {doc['article'].title}\n"
        f"Abstract: {doc['article'].abstract or ''}\n"
        f"PMID: {doc['article'].pmid}"
        for doc in retrieved_docs
    ])

    return f"""
You are a medical assistant.

Answer the question using ONLY the context below.

If the answer is not in the context, say "Not enough evidence in retrieved papers."

Always include citations using PMID.

---

Context:
{context}

---

Question:
{query}

Answer:
"""
