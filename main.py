from feed_parsers.implemented_feeds import CbcSourceFeed
from pipeline.pipeline import Pipeline

if __name__ == '__main__':
    cbc = CbcSourceFeed(url='https://www.cbc.ca/cmlink/rss-topstories')
    cbc2 = CbcSourceFeed(url='https://rss.cbc.ca/lineup/canada.xml')
    # a = (cbc.fetch())

    pipeline = Pipeline(feeds=[cbc, cbc2])
    pipeline.start()
    pass

    while 1:1