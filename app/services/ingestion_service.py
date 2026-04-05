from app.pipeline.clean_text_handler import CleanTextHandler
from app.pipeline.chunk_text_handler import ChunkTextHandler
from app.pipeline.store_chunks_handler import StoreChunksHandler


class IngestionService:
    def ingest(self, document_id: int, content: str) -> dict:
        context = {
            "document_id": document_id,
            "content": content
        }

        clean_handler = CleanTextHandler()
        chunk_handler = ChunkTextHandler(chunk_size=200)
        store_handler = StoreChunksHandler()

        clean_handler.set_next(chunk_handler).set_next(store_handler)

        return clean_handler.handle(context)