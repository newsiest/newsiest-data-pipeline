from abc import abstractmethod
from typing import Callable, Union

from feed_parsers.source_feed import SourceFeed
from models.news_article import NewsArticle


class PipelineStage:

    def __init__(self):
        self._listeners: [Callable[[NewsArticle], None]] = []

    def register_listener(self, callback: Callable[[NewsArticle], None]):
        self.listeners.append(callback)

    def emit(self, to_emit: NewsArticle):
        for l in self._listeners:
            l(to_emit)

    @abstractmethod
    def _enqueue_one(self, article: NewsArticle):
        pass

    def enqueue(self, article: Union[list[NewsArticle], NewsArticle]):
        if (isinstance(article, list)):
            [self._enqueue_one(x) for x in article]
        else:
            self._enqueue_one(article)


class Pipeline:
    def __init__(self, feeds: [SourceFeed]):
        self.feeds = []
