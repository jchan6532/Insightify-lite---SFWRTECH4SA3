from abc import ABC, abstractmethod


class BaseHandler(ABC):
    def __init__(self):
        self._next_handler = None

    def set_next(self, handler):
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, context: dict) -> dict:
        pass

    def handle_next(self, context: dict) -> dict:
        if self._next_handler:
            return self._next_handler.handle(context)
        return context