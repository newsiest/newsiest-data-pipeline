from urllib.parse import urlparse
import favicon
from time import time


def init():
    global _icons, favicon_wait_time

    _icons = {}
    favicon_wait_time = 0


def get_favicon(url: str) -> str:
    # TODO replace with redis
    start_time = time()

    global _icons, favicon_wait_time

    icon = None
    try:
        obj = urlparse(url)
        parsed = obj.scheme + '://' + obj.netloc

        if parsed in _icons:
            return _icons[parsed]

        icon = favicon.get(parsed)[0]
        _icons[parsed] = icon

    finally:
        global favicon_wait_time
        favicon_wait_time += time() - start_time
        return icon


def get_favicon_wait_time():
    global favicon_wait_time
    return favicon_wait_time