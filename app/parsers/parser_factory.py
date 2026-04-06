from app.parsers.txt_parser import TxtParser
from app.parsers.pdf_parser import PdfParser
from app.parsers.docx_parser import DocxParser

class ParserFactory:
    @staticmethod
    def create_parser(filename: str):
        normalized_name = filename.lower().strip()

        if normalized_name.endswith(".txt"):
            return TxtParser()
        
        if normalized_name.endswith(".pdf"):
            return PdfParser()

        if normalized_name.endswith(".docx"):
            return DocxParser()

        raise ValueError(f"Unsupported file type for file: {filename}")