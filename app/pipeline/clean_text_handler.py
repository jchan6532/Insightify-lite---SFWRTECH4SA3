from app.pipeline.base_handler import BaseHandler

class CleanTextHandler(BaseHandler):
    def handle(self, context: dict) -> dict:
        text = context.get("content", "")
        cleaned_text = " ".join(text.split())
        context["content"] = cleaned_text
        return self.handle_next(context)