from feed_parsers.cbc_source_feed import CbcSourceFeed

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    cbc = CbcSourceFeed(url='https://www.cbc.ca/cmlink/rss-topstories')
    print(cbc.fetch())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
