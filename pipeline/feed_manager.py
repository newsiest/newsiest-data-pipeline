from typing import Callable
from queue import Queue

from feed_parsers.source_feed import SourceFeed
from models.news_article import NewsArticle
from pipeline.pipeline import PipelineStage

FREQUENCY = 10

class FeedManager(PipelineStage):

    def __init__(self, feeds: [SourceFeed]):
        super().__init__()
        self._queue = Queue()
        self._feeds = feeds

    def start(self):
        pass

    def _enqueue_one(self, article: NewsArticle):
        pass

