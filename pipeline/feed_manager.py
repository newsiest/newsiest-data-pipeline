import sys
from concurrent.futures import thread
import time
from typing import Callable
from queue import Queue

from feed_parsers.source_feed import SourceFeed
from models.news_article import NewsArticle
from pipeline.pipeline_stage import PipelineStage
from apscheduler.schedulers.background import BackgroundScheduler
import threading
import logging

FREQUENCY = 10

class FeedManager(PipelineStage):

    def __init__(self, feeds: [SourceFeed]):
        super().__init__()
        self._queue = Queue()
        self._feeds = feeds

    def start(self):
        scheduler = BackgroundScheduler()
        scheduler.add_job(self._wait_on_queue, 'interval', seconds=0.1)

        scheduler.start()
        for f in self._feeds:
            scheduler.add_job(
                self._start_feed_thread,
                'interval',
                seconds=3,
                args=(f,)
                # jitter=5
            )


    def _enqueue_one(self, article: NewsArticle):
        pass

    def _wait_on_queue(self):
        while(not self._queue.empty()):
            self.emit(self._queue.get())

    def _start_feed_thread(self, feed: SourceFeed):
        t = threading.Thread(target=FeedManager._start_feed, args=(feed, self._queue))
        t.start()
        # t.join()

    @staticmethod
    def _start_feed(feed: SourceFeed, queue: Queue):
        start = time.time()
        articles = feed.fetch()
        if(articles):
            for a in articles:
                queue.put(a)

        print(f'Fetched from {feed.url} tag {feed.tag}, found {len(articles) if articles else 0}')

        # time.sleep(10)
        # print(time.time() - start)
        sys.exit()
        print("test")