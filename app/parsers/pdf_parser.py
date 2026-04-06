from app.parsers.base_parser import BaseParser


class PdfParser(BaseParser):
    def parse(self, raw_content: bytes) -> str:
        raise NotImplementedError("PDF parsing not implemented yet.")