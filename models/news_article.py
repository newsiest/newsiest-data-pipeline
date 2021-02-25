import datetime

class NewsArticle:
    def __init__(self, title: str = None, author: str = None, url: str = None, img_url: str = None, published: datetime = None):
        self.title = title
        self.author = author
        self.url = url
        self.img_url = img_url
        self.published = published