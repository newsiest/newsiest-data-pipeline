import datetime
import jsonpickle

class NewsArticle:
    """
    Represents a single news article
    """
    def __init__(self, title: str = None, author: str = None, url: str = None, img_url: str = None,
                 pub_date: datetime = None, tags: [str] = None, desc: str = None):
        self.title = title
        self.author = author
        self.url = url
        self.img_url = img_url
        self.pub_date = pub_date
        self.tags = tags
        self.desc = desc

    def __str__(self):
        return self.title