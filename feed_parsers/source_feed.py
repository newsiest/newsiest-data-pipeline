import logging
from abc import abstractmethod

import feedparser

import pytz
import traceback
from datetime import datetime

from models.news_article import NewsArticle, NewsSource


class SourceFeed:
    """
    Represents a generic rss feed

    Extend this class for each feed source/format
    """

    def __init__(self, url: str, tag: str = None, last_updated=None, source: NewsSource = None) -> None:
        eastern = pytz.timezone('US/Eastern')
        self.url = url
        self.last_updated: datetime = last_updated or datetime(1971, 1, 1, tzinfo=eastern)
        self.top_article_date: datetime = datetime(1971, 1, 1, tzinfo=eastern)
        self.tag = tag
        self.source = source

    def fetch(self) -> [NewsArticle]:
        try:
            feed = feedparser.parse(self.url)

            # Only refresh feed if it updated
            last_updated = self._parse_last_updated(feed)
            if last_updated and last_updated <= self.last_updated:
                return []

            # Only get new articles
            articles = list(filter(lambda art: art.pub_date >= self.last_updated,
                                   self._parse_articles(feed))) or []  # TODO use bisect to improve performance

            self.last_updated = last_updated
            self.top_article_date = articles[0].pub_date

            return articles
        except Exception as e:
            logging.error(f'Error with feed {feed.url}')
            traceback.print_exc()
            return []

    @abstractmethod
    def _parse_last_updated(self, feed: feedparser) -> datetime:
        raise NotImplementedError

    @abstractmethod
    def _parse_articles(self, feed: feedparser) -> [NewsArticle]:
        raise NotImplementedError

    @abstractmethod
    def _parse_one_img_url(self, obj):
        raise NotImplementedError
