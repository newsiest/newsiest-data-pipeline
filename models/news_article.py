import datetime

# TODO use dataclasses?

class NewsSource:
    def __init__(self, name: str, img_url: str):
        self.name = name
        self.img_url = img_url


class NewsArticle:
    """
    Represents a single news article
    """
    def __init__(self, title: str = None, author: str = None, url: str = None, img_url: str = None,
                 pub_date: datetime = None, tags: [str] = None, desc_title: str = None, desc_para: str = None,
                 source: NewsSource = None):
        self.title = title
        self.author = author
        self.url = url
        self.img_url = img_url
        self.pub_date = pub_date
        self.tags = tags
        self.desc_title = desc_title
        self.desc_para = desc_para
        self.source = source

    def __str__(self):
        return f'{self.source.name if self.source else None}, {self.title}'

    def as_dict(self):
        attrs =  self.__dict__.copy()
        attrs['source'] = self.source.__dict__
        return attrs
