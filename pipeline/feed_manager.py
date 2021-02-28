import sys
from concurrent.futures import thread
from typing import Callable
from queue import Queue

from feed_parsers.source_feed import SourceFeed
from models.news_article import NewsArticle
from pipeline.pipeline_stage import PipelineStage
from apscheduler.schedulers.background import BackgroundScheduler
import threading

FREQUENCY = 10

class FeedManager(PipelineStage):

    def __init__(self, feeds: [SourceFeed]):
        super().__init__()
        self._queue = Queue()
        self._feeds = feeds

    def start(self):
        scheduler = BackgroundScheduler()
        scheduler.add_job(self._wait_on_queue, 'interval', seconds=0.1)

        for f in self._feeds:
            scheduler.add_job(
                lambda: self._start_feed_thread(f),
                'interval',
                seconds=5
            )
        scheduler.start()


    def _enqueue_one(self, article: NewsArticle):
        pass

    def _wait_on_queue(self):
        while(not self._queue.empty()):
            self.emit(self._queue.get())

    def _start_feed_thread(self, feed: SourceFeed):
        t = threading.Thread(target=FeedManager._start_feed, args=(feed, self._queue))
        t.start()

    @staticmethod
    def _start_feed(feed: SourceFeed, queue: Queue):
        articles = feed.fetch()
        if(articles):
            for a in articles:
                queue.put(a)

        sys.exit()
        print("test")