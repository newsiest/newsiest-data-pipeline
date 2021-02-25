import feedparser
import typing
from datetime import datetime


class SourceFeed:

    def __init__(self, url: str, on_complete) -> None:
        self.url = url
        self.last_updated: datetime = None
        self.top_article_id: str = None
        self.last_id: str = None
        self.on_complete = on_complete

    def fetch(self):
        feed = feedparser.parse(self.url)

        if feed.channel.updated > self.last_updated:
            pass

        self.last_updated = feed.channel.updated
        self.on_complete()



