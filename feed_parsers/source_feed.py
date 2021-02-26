import feedparser
import typing
from datetime import datetime

from models.news_article import NewsArticle


class SourceFeed:
    """
    Represents a generic rss feed
    """

    def __init__(self, url: str, on_complete) -> None:
        self.url = url
        self.last_updated: datetime = None
        self.top_article_id: str = None
        self.last_id: str = None
        self.on_complete = on_complete

    def fetch(self) -> [NewsArticle]:
        feed = feedparser.parse(self.url)

        # Only refresh feed if it updated
        last_updated = self.__parse_last_updated()
        if last_updated <= self.last_updated:
            return []



        self.last_updated = feed.channel.updated
        self.on_complete()

    def __parse_last_updated(self, feed: feedparser):
        pass

