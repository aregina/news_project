import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news_project.settings")
django.setup()

from db.models import News, NewsText
from prjparser import textParser, urlOpen

for news in News.objects.iterator():
    html = urlOpen.get_html(news.url)
    if html:
        text = textParser.get_text_from_html(html)
        NewsText.objects.create(news=news, text=text)

