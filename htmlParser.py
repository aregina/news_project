import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news_project.settings")
django.setup()

from db.models import News, NewsText
import urllib.request as url
from prjparser import textParser

for news in News.objects.iterator():
    with url.urlopen(news.url) as a:
        txt = a.read()
        if a.getheader('Content-Encoding') == 'gzip':
            import gzip

            txt = gzip.decompress(txt)
    encodings = ["utf8", "cp1251"]
    for encode in encodings:
        try:
            txt = txt.decode(encoding=encode)
        except UnicodeDecodeError:
            print("error")
            continue
        else:
            text = textParser.get_text_from_html(txt)
            news_text = NewsText(news=news, text=text)
            news_text.save()
            break
        print("never print")
