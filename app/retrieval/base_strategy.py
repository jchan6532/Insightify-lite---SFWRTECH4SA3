from abc import ABC, abstractmethod


class RetrievalStrategy(ABC):
    @abstractmethod
    def retrieve(self, question: str, limit: int = 3) -> list[dict]:
        pass