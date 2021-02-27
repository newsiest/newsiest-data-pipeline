from feed_parsers.source_feed import SourceFeed
from models.news_article import NewsArticle
from pipeline.feed_manager import FeedManager


class Pipeline:
    def __init__(self, feeds: [SourceFeed]):
        # self.feeds = feeds
        self.feed_manager = FeedManager(feeds)
        self.feed_manager.register_listener(self.pr)

    def pr(self, article: NewsArticle):
        print(article)

    def start(self):
        self.feed_manager.start()
