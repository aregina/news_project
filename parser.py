from utils import DjangoSetup
from db.models import News, RssChannels, ASources
from prjparser import aParser, rssParser, model
from datetime import datetime
from django.db import transaction, models


def add_news(news_data: model.NewsData) -> News:
    if not News.objects.filter(url=news_data.url)[:1].exists():
        return News.objects.create(site=news_data.site_obj,
                                   title=news_data.title,
                                   url=news_data.url,
                                   pub_date=news_data.pub_date,
                                   summary=news_data.summary)


# TODO добавить проверку типов передоваемых объектов
def get_news(source: models.Model, parser: model.Parser):
    """
    :type source: <class 'django.db.models.base.ModelBase'>
    :type parser: parser method
    """
    for entry in source.objects.iterator():
        n = 0
        with transaction.atomic():  # атомарная транзакция
            for news in parser.parse(entry.url):
                news.site_obj = entry.site
                if add_news(news):
                    n += 1
        if n:
            print("[{}] {} news add from {} {}".format(datetime.now(), n, entry, entry.site.name))


def main():
    get_news(RssChannels, rssParser)
    get_news(ASources, aParser)


if __name__ == "__main__":
    main()
