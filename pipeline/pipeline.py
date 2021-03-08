from feed_parsers.source_feed import SourceFeed
from models.news_article import NewsArticle
from pipeline.feed_manager import FeedManager
from pipeline.pipeline_stage import PipelineStage


class Pipeline:
    """
    Represents the ETL pipeline cumulatively, aggregating all stages
    """
    def __init__(self, stages: [PipelineStage]):
        """
        :param stages: PipelinStages in order of desired execution
        """
        self.stages: PipelineStage = stages

    def pr(self, articles: [NewsArticle]):
        [print(x) for x in articles]

    def _chain_feeds(self):
        """
        Set subsequent pipeline stages as listeners
        """
        for i in range(1, len(self.stages)):
            self.stages[i-1].register_listener(self.stages[i].process)

        self.stages[-1].register_listener(self.pr) # TODO remove

    def start(self):
        """
        Begin the pipeline
        """
        self._chain_feeds()
        self.stages[0].start()