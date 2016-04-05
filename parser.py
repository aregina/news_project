import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news_project.settings")
django.setup()

from db.models import *
import feedparser
from datetime import datetime as dt
from time import mktime
from prjparser import aParser, urlOpen, textParser

for rss in RssChannels.objects.iterator():
    n = 0
    parser = feedparser.parse(rss.url)
    for news in parser['items']:
        url = aParser.remove_query_from_url(news['link'])
        if not News.objects.filter(url=url)[:1].exists():
            News.objects.create(site=rss.site,
                                title=news['title'],
                                url=url,
                                pub_date=dt.fromtimestamp(mktime(news['published_parsed'])),
                                summary=news.get('summary', None))
            n += 1
    if n:
        print("[{}] {} news add from {}".format(dt.now(), n, parser['feed'].title))

for source in ASources.objects.iterator():
    html_code = urlOpen.get_html(source.url)
    html_code = textParser.tags_filter_head_and_script(html_code)
    for url, text in aParser.get_url_and_url_text(html_code, source.url):
        if not News.objects.filter(url=url)[:1].exists():
            News.objects.create(site=source.site,
                                title=text,
                                url=url,
                                pub_date=dt.now(),
                                summary=None)
