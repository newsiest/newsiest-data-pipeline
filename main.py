import yaml
import os
from datetime import time

from feed_parsers.implemented_feeds import CbcSourceFeed
from pipeline.pipeline import Pipeline


SOURCE_CLASSES = {
    'cbc': CbcSourceFeed
}

def load_feeds(file_name: str):
    with open(file_name, 'r') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
        print(data)
        for source in data:


            pass


if __name__ == '__main__':
    load_feeds('feeds.yaml')
    cbc = CbcSourceFeed(url='https://www.cbc.ca/cmlink/rss-topstories', tag='cbc1')
    cbc2 = CbcSourceFeed(url='https://rss.cbc.ca/lineup/canada.xml', tag='cbc2')
    # a = (cbc.fetch())
    feeds = [cbc, cbc2]

    for i in range(1):
        feeds.append(CbcSourceFeed(url='https://rss.cbc.ca/lineup/canada.xml', tag=str(i)))

    # logging.basicConfig(level=logging.DEBUG)
    pipeline = Pipeline(feeds=feeds)
    pipeline.start()

