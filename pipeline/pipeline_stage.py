from abc import abstractmethod
from typing import Callable, Union

from models.news_article import NewsArticle


class PipelineStage:

    def __init__(self):
        self._listeners: [Callable[[NewsArticle], None]] = []

    def register_listener(self, callback: Callable[[NewsArticle], None]):
        self._listeners.append(callback)

    def emit(self, to_emit: NewsArticle):
        for l in self._listeners:
            l(to_emit)

    # TODO add type hints
    def process(self, to_process: []):
        self.emit(self._process_one(x) for x in to_process)

    @abstractmethod
    def _process_one(self, to_process):
        raise NotImplementedError()

