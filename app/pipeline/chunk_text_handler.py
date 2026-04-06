from app.pipeline.base_handler import BaseHandler


class ChunkTextHandler(BaseHandler):
    def __init__(self, chunk_size: int = 50):
        super().__init__()
        self.chunk_size = chunk_size

    def handle(self, context: dict) -> dict:
        text = context.get("content", "")
        words = text.split()

        chunks = []
        for i in range(0, len(words), self.chunk_size):
            chunk_words = words[i:i + self.chunk_size]
            chunks.append(" ".join(chunk_words))

        context["chunks"] = chunks
        return self.handle_next(context)