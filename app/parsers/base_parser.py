from abc import ABC, abstractmethod


class BaseParser(ABC):
    @abstractmethod
    def parse(self, raw_content: str) -> str:
        pass