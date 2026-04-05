from app.retrieval.base_strategy import RetrievalStrategy
from app.db import get_connection


class FullScanRetrievalStrategy(RetrievalStrategy):
    def retrieve(self, question: str, limit: int = 3) -> list[dict]:
        conn = None
        cur = None

        try:
            conn = get_connection()
            cur = conn.cursor()

            cur.execute(
                """
                SELECT c.id, c.document_id, d.title, c.chunk_index, c.chunk_text
                FROM chunks c
                JOIN documents d ON c.document_id = d.id
                ORDER BY c.document_id DESC, c.chunk_index ASC
                LIMIT %s
                """,
                (limit,)
            )

            rows = cur.fetchall()

            results = []
            for row in rows:
                results.append({
                    "chunk_id": row[0],
                    "document_id": row[1],
                    "document_title": row[2],
                    "chunk_index": row[3],
                    "chunk_text": row[4]
                })

            return results

        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()