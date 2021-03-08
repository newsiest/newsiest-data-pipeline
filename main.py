import os
from datetime import datetime
import time
import sys
import yaml
from dateutil import parser as date_parser
import logging

from feed_parsers.implemented_feeds import CbcSourceFeed
from feed_parsers.source_feed import SourceFeed
from pipeline.feed_manager import FeedManager
from pipeline.export_manager import ExportManager
from pipeline.pipeline import Pipeline
from pipeline.tagger import Tagger

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
    start_time = time.time()
    logging.basicConfig(format='[%(levelname)s] %(asctime)s - %(filename)s:%(funcName)s - %(message)s',
                        level=logging.INFO, stream=sys.stdout)

    logging.info('Woken up')
    last_run_date = unpack_args(sys.argv)
    logging.info(f'Last Run at: {last_run_date}')

    feeds = load_feeds('feeds.yml', last_run_date)
    logging.info(f'Loading ({len(feeds)}) feeds...')

    Pipeline(
        stages = [
            FeedManager(feeds=feeds),
            Tagger(),
            ExportManager()
        ],
        print_articles = not os.getenv('SUPPRESS_PRINT')
    ).start()

    logging.info(f'Shutting down, total execution time: {time.time()- start_time}s')

