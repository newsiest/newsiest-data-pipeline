import logging
import threading
from datetime import time

from feed_parsers.implemented_feeds import CbcSourceFeed
from pipeline.pipeline import Pipeline

def test():
    time.sleep(2)
    print("done")
    import sys
    sys.exit()


if __name__ == '__main__':
    cbc = CbcSourceFeed(url='https://www.cbc.ca/cmlink/rss-topstories', tag='cbc1')
    cbc2 = CbcSourceFeed(url='https://rss.cbc.ca/lineup/canada.xml', tag='cbc2')
    # a = (cbc.fetch())
    feeds = [cbc, cbc2]

    # for i in range(60):
    #     feeds.append(CbcSourceFeed(url='https://rss.cbc.ca/lineup/canada.xml', tag=str(i)))

    # logging.basicConfig(level=logging.DEBUG)
    pipeline = Pipeline(feeds=feeds)
    pipeline.start()

    # t = threading.Thread(target=test)
    # t.start()
    # t.join()


    while 1:1