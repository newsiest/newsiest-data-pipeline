from urllib.parse import urlparse
import favicon

_icons = {}


def get_favicon(url: str) -> str:
    # TODO replace with redis

    try:
        obj = urlparse(url)
        parsed = obj.scheme + '://' + obj.netloc

        if parsed in _icons:
            return _icons[parsed]

        icon = favicon.get(parsed)[-1]
        _icons[parsed] = icon
        return icon

    except:
        return None
