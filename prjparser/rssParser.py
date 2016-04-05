import feedparser
from prjparser import aParser, model
from datetime import datetime as dt
from time import mktime


def parse(rss_url):
    parsed_data = feedparser.parse(rss_url)
    for rss_entry in parsed_data['items']:
        url = aParser.remove_query_from_url(rss_entry['link'])
        yield model.NewsData(url=url,
                             title=rss_entry['title'],
                             pub_date=dt.fromtimestamp(mktime(rss_entry['published_parsed'])),
                             summary=rss_entry.get('summary', None))
