import yaml
from feed_parsers.implemented_feeds import CbcSourceFeed
from feed_parsers.source_feed import SourceFeed
from pipeline.feed_manager import FeedManager
from pipeline.pipeline import Pipeline

SOURCE_CLASSES = {
    'cbc': CbcSourceFeed
}

def load_feeds(file_name: str) -> [SourceFeed]:
    """
    Loads feed urls from yaml file
    """
    feeds = []
    with open(file_name, 'r') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
        for source in data:
            assert source in SOURCE_CLASSES
            feeds += [SOURCE_CLASSES[source](url=url) for url in data[source]]
    return feeds

if __name__ == '__main__':
    feeds = load_feeds('feeds.yaml')
    Pipeline(stages=[
        FeedManager(feeds=feeds)
    ]).start()

