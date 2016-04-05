import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news_project.settings")
django.setup()

from prjparser import aParser
from db.models import News

for news in News.objects.iterator():
    url = aParser.remove_query_from_url(news.url)
    if len(url) != len(news.url):
        if not News.objects.filter(url=url)[:1].exists():
            print("update news id{}\t{}".format(str(news.id),news.url))
            news.url = url
            news.save()
        else:
            print("delete news id{}\t{}".format(str(news.id),news.url))
            news.delete()

