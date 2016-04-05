import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news_project.settings")
django.setup()

from db.models import News, NewsText, UrlInText
from prjparser import textParser, urlOpen, aParser


def parse_news():
    for news in News.objects.iterator():
        if hasattr(news, 'newstext'): continue
        html = urlOpen.get_html(news.url)
        if html:
            print(str(news.id) + "     ", end='\r')
            text = textParser.get_text_from_html(html)
            NewsText.objects.create(news=news, text=text)


def parse_news_text(news_text: NewsText):
    print(str(news_text.pk) + "     ", end='\r')
    for url in aParser.get_a_from_news_text(news_url=news_text.news.url, text=news_text.text):
        url_in_text = UrlInText.objects.filter(url=url)[:1]
        if url_in_text.exists():
            url_in_text = url_in_text[0]
        else:
            url_in_text = UrlInText.objects.create(url=url)
        url_in_text.news.add(news_text.news)
    news_text.text = aParser.remove_all_tags(news_text.text)
    news_text.is_parsed = True
    news_text.save()


def main():

    parse_news()

    for news_text in NewsText.objects.filter(is_parsed=False).iterator():
        parse_news_text(news_text)

if __name__ == "__main__":
    main()
