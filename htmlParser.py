from utils import DjangoSetup # setup django environment
from db.models import News, NewsText, UrlInText
from prjparser import textParser, urlOpen, aParser
from django.db import transaction


@transaction.atomic
def parse_news(n=None):

    for news in News.objects.filter(is_parsed=False)[:n].iterator():
        print(str(news.id) + "     ", end='\n')
        html = urlOpen.get_html(news.url)  # 0.19 - 2.5 s
        if html:
            text = textParser.get_text_from_html(html)  # 0.0099 - 0.026 s
            NewsText.objects.create(news=news, text=text)
            news.is_parsed = True
            news.save()  # 0.004 with atomic and 0.23 without


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


    parse_news(10)
    # for news_text in NewsText.objects.filter(is_parsed=False).iterator():
    #     parse_news_text(news_text)

if __name__ == "__main__":
    main()
