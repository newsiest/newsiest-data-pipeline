import regex
from models.news_article import NewsArticle
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
            desc_title = regex.search('(?<=title=[\'"])([\s\w.,:!?\\\/-]*)', e.description)
            desc_title = desc_title.group(0) if desc_title else ''

            desc_para = regex.search('(?<=<p>)(.*?)(?=<\/p>)', e.description).group(0)

            articles.append(NewsArticle(
                title=e.title,
                author=e.author if e.author else 'CBC News',
                url=e.links[0].href,
                pub_date=date_parser.parse(e.published),
                desc=desc_title + desc_para
            ))
        return articles


class NytSourceFeed(SourceFeed):
    def _parse_last_updated(self, feed: feedparser) -> datetime:
        pass

    def _parse_articles(self, feed: feedparser) -> [NewsArticle]:
        pass
