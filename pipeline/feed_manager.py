import logging
import time
from feed_parsers.source_feed import SourceFeed
from pipeline.pipeline_stage import PipelineStage


class FeedManager(PipelineStage):

    def __init__(self, feeds: [SourceFeed]):
        super().__init__()
        self._feeds = feeds

    def start(self):
        logging.info('Starting feed fetch...')

        start = time.time()
        articles = []

        for f in self._feeds:
            articles += f.fetch()

        logging.info(f'Finished fetch. Took: {time.time() - start}s, Found: {len(articles)} new articles')
        self.emit(articles)

    def _process_one(self, to_process):
        raise NotImplementedError
