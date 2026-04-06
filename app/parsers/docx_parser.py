from io import BytesIO
from docx import Document
from app.parsers.base_parser import BaseParser


class DocxParser(BaseParser):
    def parse(self, raw_content: bytes) -> str:
        file_stream = BytesIO(raw_content)
        document = Document(file_stream)

        paragraphs = []
        for paragraph in document.paragraphs:
            text = paragraph.text.strip()
            if text:
                paragraphs.append(text)

        return "\n".join(paragraphs)