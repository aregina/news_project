import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news_project.settings")
django.setup()

from db.models import News, NewsText
from prjparser import textParser, urlOpen

for news in News.objects.iterator():
    txt = urlOpen.read(news.url)
    if txt:
        text = textParser.get_text_from_html(txt)
        news_text = NewsText(news=news, text=text)
        news_text.save()
