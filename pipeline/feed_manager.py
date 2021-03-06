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
import os

FREQUENCY = 10

class FeedManager(PipelineStage):

    def __init__(self, feeds: [SourceFeed]):
        super().__init__()
        self._feeds = feeds

    def start(self):
        start = time.time()
        articles = []

        for f in self._feeds:
            articles += f.fetch()

        print(f'Took: {time.time() - start}')
        self.emit(articles)

    def _process_one(self, to_process):
        raise NotImplementedError

