from app.parsers.txt_parser import TxtParser


class ParserFactory:
    @staticmethod
    def create_parser(filename: str):
        normalized_name = filename.lower().strip()

        if normalized_name.endswith(".txt"):
            return TxtParser()

        raise ValueError(f"Unsupported file type for file: {filename}")