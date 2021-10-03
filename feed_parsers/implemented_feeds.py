import logging
import traceback
from abc import ABC

from models.news_article import NewsArticle, NewsSource
import feedparser
import datetime
from dateutil import parser as date_parser
from feed_parsers.source_feed import SourceFeed
from cache_util import get_favicon

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
        if 'updated' in feed:
            return date_parser.parse(feed.updated)
        elif 'channel' in feed and 'updated' in feed.channel:
            return date_parser.parse(feed.channel.updated)
        else:
            logging.error(f'{feed.url} has no last updated val!')
            return None

    def _feed_has_updated(self, feed):
        last_updated = self._parse_last_updated(feed)
        return last_updated and last_updated > self.last_updated

    def _parse_articles(self, feed_dict: feedparser) -> [NewsArticle]:

        if not self.source:
            self.source = NewsSource(name=feed_dict.feed.title)

        if not self.source.logo_url:
            icon = get_favicon(feed_dict.url)
            if icon:
                self.source.logo_url = icon
            elif 'image' in feed_dict.feed:
                self.source.logo_url = feed_dict.feed['image'].href

        articles = []
        for e in feed_dict.entries:
            try:
                articles.append(NewsArticle(
                    title=e.title,
                    author=e.author if 'author' in e and e.author else self.source.name,
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



