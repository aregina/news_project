from datetime import datetime
from utils import DjangoSetup
from db.models import News, RssChannels, ASources
from prjparser import aParser, rssParser, model
from prjparser import multiproc


def add_news(news_data: model.NewsData) -> News:
    if not News.objects.filter(url=news_data.url)[:1].exists():
        return News.objects.create(site=news_data.site_obj,
                                   title=news_data.title,
                                   url=news_data.url,
                                   pub_date=news_data.pub_date,
                                   summary=news_data.summary)


class RssParser(multiproc.MultiProc):
    def writer(self, container):
        n = 0
        rss, news_list = container
        for news in news_list:
            if add_news(news):
                n += 1
        if n:
            print("[{}] {} news add from {} {}".format(datetime.now(), n, rss, rss.site.name))

    def worker(self, rss: RssChannels):
        news_list = []
        for news in rssParser.parse(rss.url):
            news.site_obj = rss.site
            news_list.append(news)
        if news_list:
            return rss, news_list

    task_manager = RssChannels.objects.iterator


class ASourceParser(multiproc.MultiProc):
    def writer(self, container):
        n = 0
        a_source, news_list = container
        for news in news_list:
            if add_news(news):
                n += 1
        if n:
            print("[{}] {} news add from {} {}".format(datetime.now(), n, a_source, a_source.site.name))

    def worker(self, source: ASources):
        news_list = []
        for news in aParser.parse(source.url):
            news.site_obj = source.site
            news_list.append(news)
        if news_list:
            return source, news_list

    task_manager = ASources.objects.iterator


def main():
    RssParser().run()
    ASourceParser().run()


if __name__ == "__main__":
    main()
