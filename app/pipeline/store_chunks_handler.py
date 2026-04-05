from app.pipeline.base_handler import BaseHandler
from app.db import get_connection


class StoreChunksHandler(BaseHandler):
    def handle(self, context: dict) -> dict:
        document_id = context.get("document_id")
        chunks = context.get("chunks", [])

        conn = None
        cur = None

        try:
            conn = get_connection()
            cur = conn.cursor()

            for index, chunk_text in enumerate(chunks):
                cur.execute(
                    """
                    INSERT INTO chunks (document_id, chunk_index, chunk_text)
                    VALUES (%s, %s, %s)
                    """,
                    (document_id, index, chunk_text)
                )

            conn.commit()
            context["stored_chunk_count"] = len(chunks)
            return self.handle_next(context)

        except Exception:
            if conn:
                conn.rollback()
            raise

        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()