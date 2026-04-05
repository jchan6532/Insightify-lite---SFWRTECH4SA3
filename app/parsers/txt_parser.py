from app.parsers.base_parser import BaseParser


class TxtParser(BaseParser):
    def parse(self, raw_content: str) -> str:
        return raw_content.strip()