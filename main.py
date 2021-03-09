from datetime import datetime
import sys
import yaml
from dateutil import parser as date_parser

from feed_parsers.implemented_feeds import CbcSourceFeed
from feed_parsers.source_feed import SourceFeed
from pipeline.feed_manager import FeedManager
from pipeline.pipeline import Pipeline

SOURCE_CLASSES = {
    'cbc': CbcSourceFeed
}

def load_feeds(file_name: str, last_updated: datetime) -> [SourceFeed]:
    """
    Load feed urls from yaml file
    """
    feeds = []
    with open(file_name, 'r') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
        for source in data:
            assert source in SOURCE_CLASSES
            feeds += [SOURCE_CLASSES[source](url=url, last_updated=last_updated) for url in data[source]]
    return feeds

def unpack_args(args: [str]) -> str:
    """
    Load date from command line args
    """
    return date_parser.parse(args[1]) if len(args) > 1 and args[1] != '' else None

if __name__ == '__main__':
    last_run_date = unpack_args(sys.argv)
    feeds = load_feeds('feeds.yaml', last_run_date)
    Pipeline(stages=[
        FeedManager(feeds=feeds)
    ]).start()

