import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news_project.settings")
django.setup()

from db.models import *
import feedparser
from datetime import datetime as dt
from time import mktime
from prjparser import aParser, urlOpen, textParser

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

for link in ASources.objects.iterator():
    html_code = urlOpen.get_html(link.url)
    html_code = textParser.tags_filter_head_and_script(html_code)
    for url, text in aParser.get_url_and_url_text(html_code,link.url):
        if url.startswith(link.url):
            if not News.objects.filter(url=url).exists():
                News.objects.create(site=link.site,
                                    title=text,
                                    url=url,
                                    pub_date=dt.now(),
                                    summary=None)
