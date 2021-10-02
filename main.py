import os
from datetime import datetime
import time
import sys
import yaml
from dateutil import parser as date_parser
import logging

from feed_parsers.implemented_feeds import CbcSourceFeed, DefaultSourceFeed
from feed_parsers.source_feed import SourceFeed
from models.news_article import NewsSource
from pipeline.feed_manager import FeedManager
from pipeline.export_manager import ExportManager
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
        for source_data in data['sources']:
            source_obj = NewsSource(source_data['name'], source_data['logo-url'])
            feed_cls = SOURCE_CLASSES[source_data['parser']] if source_data['parser'] in SOURCE_CLASSES \
                else DefaultSourceFeed

            feeds += [feed_cls(url=url, last_updated=last_updated) for url in source_data['feeds']]

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

    feeds = load_feeds('feeds_new.yml', last_run_date)
    logging.info(f'Loading ({len(feeds)}) feeds...')

    Pipeline(
        stages=[
            FeedManager(feeds=feeds),
            # ExportManager()
        ],
        print_articles=not os.getenv('SUPPRESS_PRINT')
    ).start()

    logging.info(f'Shutting down, total execution time: {time.time() - start_time}s')
