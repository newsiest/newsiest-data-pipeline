import traceback
from abc import ABC

from models.news_article import NewsArticle, NewsSource
import feedparser
import datetime
from dateutil import parser as date_parser
from feed_parsers.source_feed import SourceFeed


class CbcSourceFeed(SourceFeed):

    def _parse_last_updated(self, feed: feedparser) -> datetime:
        return date_parser.parse(feed.channel.updated)

    def _parse_articles(self, feed: feedparser) -> [NewsArticle]:
        articles = []
        for e in feed.entries:
            articles.append(NewsArticle(
                title=e.title,
                author=e.author if e.author else 'CBC News',
                url=e.links[0].href,
                pub_date=date_parser.parse(e.published),
                source=self.source
            ))
        return articles


class NytSourceFeed(SourceFeed):
    def _parse_last_updated(self, feed: feedparser) -> datetime:
        pass

    def _parse_articles(self, feed: feedparser) -> [NewsArticle]:
        pass


class DefaultSourceFeed(SourceFeed):

    def _parse_last_updated(self, feed: feedparser) -> datetime:
        return date_parser.parse(feed.channel.updated)

    def _parse_articles(self, feed_dict: feedparser) -> [NewsArticle]:

        if not self.source:
            self.source = NewsSource(name=feed_dict.title)

        if not self.source.logo_url:
            if 'image' in feed_dict.feed:
                self.source.logo_url = feed_dict.feed['image'].href

        articles = []
        for e in feed_dict.entries:
            try:
                articles.append(NewsArticle(
                    title=e.title,
                    author=e.author if e.author else self.source.name,
                    url=e.link,
                    pub_date=date_parser.parse(e.published),
                    source=self.source,
                    img_url=self._parse_one_img_url(e)
                ))
            except Exception as e:
                traceback.print_exc()

        return articles

    def _parse_one_img_url(self, obj) -> str:
        if 'media_thumbnail' in obj:
            return obj['media_thumbnail']
        elif len(obj.links) > 1:
            return obj.links[1].href
        else:
            return None



