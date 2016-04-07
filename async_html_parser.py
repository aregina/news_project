from utils import DjangoSetup  # setup django environment
from db.models import News, NewsText, UrlInText
from prjparser import textParser, urlOpen, aParser
from prjparser import multiproc


class HtmlParser(multiproc.MultiProc):
    def task_manager(self):
        for item in News.objects.filter(is_parsed=False)[:].iterator():
            yield item

    def worker(self, news):
        print(str(news.id) + "     ", end='\n')
        html = urlOpen.get_html(news.url)
        if html:
            text = textParser.get_text_from_html(html)
            return NewsText(news=news, text=text)

    def writer(self, news_text):
        news_text.save()
        news_text.news.is_parsed = True
        news_text.news.save()


class NewsTextParser(multiproc.MultiProc):
    def task_manager(self):
        for news_text in NewsText.objects.filter(is_parsed=False).iterator():
            yield news_text

    def worker(self, news_text: NewsText):
        url_list = []
        for url in aParser.get_a_from_news_text(news_url=news_text.news.url, text=news_text.text):
            url_list.append(url)

        return [news_text, url_list]

    def writer(self, container):
        news_text_obj = container[0]
        url_list = container[1]
        for url in url_list:
            url_in_text = UrlInText.objects.filter(url=url)[:1]
            if url_in_text.exists():
                url_in_text = url_in_text[0]
            else:
                url_in_text = UrlInText(url=url)
                url_in_text.save()
            url_in_text.news.add(news_text_obj.news)
        news_text_obj.text = aParser.remove_all_tags(news_text_obj.text)
        news_text_obj.is_parsed = True
        news_text_obj.save()
        print("news_text_id {}".format(news_text_obj.pk))


def main():
    HtmlParser(process_number=20).run()
    NewsTextParser().run()


if __name__ == "__main__":
    main()
