from app.parsers.txt_parser import TxtParser


class ParserFactory:
    @staticmethod
    def create_parser(file_type: str):
        normalized_type = file_type.lower().strip()

        if normalized_type == "txt":
            return TxtParser()

        raise ValueError(f"Unsupported file type: {file_type}")