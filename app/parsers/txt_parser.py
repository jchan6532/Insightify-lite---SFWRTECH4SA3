from app.parsers.base_parser import BaseParser


class TxtParser(BaseParser):
    def parse(self, raw_content: bytes) -> str:
        return raw_content.decode("utf-8").strip()