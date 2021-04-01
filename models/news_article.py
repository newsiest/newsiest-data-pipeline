import datetime
import jsonpickle

class NewsSource:
    """
    Represents a news source (ie CNN, CBC, etc)
    """
    def __init__(self, name: str = None, logo_url = None):
        self.name = name
        self.logo_url = logo_url
        self.slug = name.lower().replace(' ', '-')

class NewsArticle:
    """
    Represents a single news article
    """
    def __init__(self, title: str = None, author: str = None, url: str = None, img_url: str = None, pub_date: datetime = None, source: NewsSource = None):
        self.title = title
        self.author = author
        self.url = url
        self.img_url = img_url
        self.pub_date = pub_date
        self.source = source

    def __str__(self):
        return self.title