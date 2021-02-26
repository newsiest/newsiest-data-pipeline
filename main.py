from feed_parsers.implemented_feeds import CbcSourceFeed

if __name__ == '__main__':
    cbc = CbcSourceFeed(url='https://www.cbc.ca/cmlink/rss-topstories')
    a = (cbc.fetch())
    pass