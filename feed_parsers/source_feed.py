import feedparser
import typing
import abc
import traceback
from datetime import datetime
from models.news_article import NewsArticle

class SourceFeed:
    """
    Represents a generic rss feed
    """

    def __init__(self, url: str) -> None:
        self.url = url
        self.last_updated: datetime = datetime(1971, 1, 1)
        self.top_article_date: datetime = datetime(1971, 1, 1)
        # self.on_complete = on_complete

    def fetch(self) -> [NewsArticle]:
        try:
            feed = feedparser.parse(self.url)

            # Only refresh feed if it updated

            last_updated = self._parse_last_updated(feed)
            if last_updated <= self.last_updated:
                return []

            # Only get new articles
            articles = self._parse_articles(feed)
            articles = filter(lambda art: art.pub_date >= self.top_article_date) # TODO use bisect to improve performance

            self.last_updated = last_updated
            self.top_article_date = articles[0].pub_date

            # self.on_complete()
            return articles
        except Exception as e:
            traceback.print_exc()
            return []

    def _parse_last_updated(self, feed: feedparser) -> datetime:
        raise NotImplementedError
        pass

    def _parse_articles(self, feed: feedparser) -> [NewsArticle]:
        pass

