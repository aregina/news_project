import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news_project.settings")
django.setup()

from db.models import *
import feedparser
from datetime import datetime as dt
from time import mktime

for rss in RssChannels.objects.iterator():
    parser = feedparser.parse(rss.url)
    n = 0
    for news in parser['items']:
        if not News.objects.filter(url=news['link']).exists():
            News.objects.create(site=rss.site,
                                title=news['title'],
                                url=news['link'],
                                pub_date=dt.fromtimestamp(mktime(news['published_parsed'])),
                                summary=news.get('summary', None))
            n += 1
    if n:
        print("[{}] {} news add from {}".format(dt.now(), n, parser['feed'].title))
