from feed_parsers.source_feed import SourceFeed
from models.news_article import NewsArticle
from pipeline.feed_manager import FeedManager


class Pipeline:
    """
    Represents the ETL pipeline cumulatively, aggregating all stages
    """

    def __init__(self, feeds: [SourceFeed]):
        # self.feeds = feeds
        self.feed_manager = FeedManager(feeds)
        self.feed_manager.register_listener(self.pr)

    def pr(self, articles: [NewsArticle]):
        [print(x) for x in articles]
        pass

    def start(self):
        self.feed_manager.start()