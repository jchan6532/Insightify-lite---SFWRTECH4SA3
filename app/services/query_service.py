from openai import OpenAI

from app.retrieval.keyword_strategy import KeywordRetrievalStrategy
from app.retrieval.full_scan_strategy import FullScanRetrievalStrategy
from app.config import OPENAI_API_KEY


class QueryService:
    def __init__(self, strategy_name: str = "keyword"):
        if strategy_name == "full_scan":
            self.strategy = FullScanRetrievalStrategy()
        else:
            self.strategy = KeywordRetrievalStrategy()

    def answer_question(self, question: str, limit: int = 3) -> dict:
        chunks = self.strategy.retrieve(question=question, limit=limit)

        if not chunks:
            return {
                "answer": "No relevant document chunks were found.",
                "references": []
            }

        context_text = "\n\n".join(
            [
                f"[Document: {chunk['document_title']}, Chunk {chunk['chunk_index']}] {chunk['chunk_text']}"
                for chunk in chunks
            ]
        )

        client = OpenAI(
            api_key=OPENAI_API_KEY
        )

        prompt = f"""
You are answering a question using only the provided document excerpts.

Question:
{question}

Document excerpts:
{context_text}

Return a concise answer based only on the excerpts.
"""

        try:
            response = client.responses.create(
                model="gpt-4.1-mini",
                input=prompt
            )
            answer = response.output_text
        except Exception:
            answer = f"OpenAI unavailable. Retrieved content:\n\n{context_text}"

        references = []
        for chunk in chunks:
            references.append({
                "document_id": chunk["document_id"],
                "document_title": chunk["document_title"],
                "chunk_index": chunk["chunk_index"]
            })

        return {
            "answer": answer,
            "references": references
        }