import logging

from feed_parsers.source_feed import SourceFeed
from models.news_article import NewsArticle
from pipeline.feed_manager import FeedManager
from pipeline.pipeline_stage import PipelineStage


class Pipeline:
    """
    Represents the ETL pipeline cumulatively, aggregating all stages
    """
    def __init__(self, stages: [PipelineStage], print_articles: bool = False):
        """
        :param stages: PipelineStages in order of desired execution
        :param print_articles: print article titles as they appear
        """
        self.stages: PipelineStage = stages
        self.print_articles = print_articles

    def print_titles(self, articles: [NewsArticle]):
        [print(f'\t{x}') for x in articles]

    def _chain_feeds(self):
        """
        Set subsequent pipeline stages as listeners
        """
        for i in range(1, len(self.stages)):
            self.stages[i-1].register_listener(self.stages[i].process)

        if(self.print_articles):
            self.stages[-1].register_listener(self.print_titles)

    def start(self):
        """
        Begin the pipeline
        """
        logging.info("Starting pipeline...")
        self._chain_feeds()
        self.stages[0].start()