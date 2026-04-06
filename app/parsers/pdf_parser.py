from io import BytesIO
from pypdf import PdfReader
from app.parsers.base_parser import BaseParser


class PdfParser(BaseParser):
    def parse(self, raw_content: bytes) -> str:
        file_stream = BytesIO(raw_content)
        reader = PdfReader(file_stream)

        pages_text = []

        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                pages_text.append(extracted.strip())

        if not pages_text:
            raise ValueError("No readable text could be extracted from the PDF.")

        return "\n".join(pages_text)