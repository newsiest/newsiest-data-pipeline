from models.news_article import NewsArticle, NewsSource
import feedparser
import datetime
from dateutil import parser as date_parser
from feed_parsers.source_feed import SourceFeed


class CbcSourceFeed(SourceFeed):
    source = NewsSource(name='CBC News')

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
