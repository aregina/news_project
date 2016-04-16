from abc import ABCMeta, abstractstaticmethod
from collections import Iterable


class NewsData(object):
    def __init__(self, url, title, pub_date, site_obj=None, summary=None):
        self.url = url
        self.title = title
        self.pub_date = pub_date
        self.summary = summary
        self.site_obj = site_obj


class Parser(metaclass=ABCMeta):
    @abstractstaticmethod
    def parse(self, source_url: str) -> Iterable:
        raise NotImplemented
