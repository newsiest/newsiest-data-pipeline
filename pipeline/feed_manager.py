import logging
import time
from feed_parsers.source_feed import SourceFeed
from pipeline.pipeline_stage import PipelineStage
from tqdm import tqdm

class FeedManager(PipelineStage):

    def __init__(self, feeds: [SourceFeed]):
        super().__init__()
        self._feeds = feeds

    def start(self):
        logging.info('Starting feed fetch...')

        start = time.time()
        articles = []

        with tqdm(total=len(self._feeds), position=0, leave=True) as pbar:
            for f in self._feeds:
                pbar.set_description(f'Updating feed {f.url}', refresh=True)
                articles += f.fetch()
                pbar.update()

            pbar.set_description('Done', refresh=True)

        logging.info(f'Finished fetch. Took: {time.time() - start}s, Found: {len(articles)} new articles')
        self.emit(articles)

    def _process_one(self, to_process):
        raise NotImplementedError
