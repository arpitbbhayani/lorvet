from news_handler import NewsHandler
from default_handler import DefaultHandler


def get_handler(category):
    m = {
        'NEWS': NewsHandler()
    }
    return m.get(category, DefaultHandler())
