from utils import DjangoSetup  # setup django environment
from db.models import News, NewsText, UrlInText
from prjparser import textParser, urlOpen, aParser
from prjparser import multiproc, text_prerparer

# TODO надо объеденить классы или както переделеть логику

class HtmlParser(multiproc.MultiProc):
    """
    Extract news text from html page
    """
    task_manager = News.objects.filter(is_parsed=False).iterator

    @staticmethod
    def worker(news):
        print(str(news.id) + "     ", end='\n')
        html = urlOpen.get_html(news.url)
        if html:
            text = textParser.get_text_from_html(html)
            return NewsText(news=news, text=text)

    @staticmethod
    def writer(news_text):
        news_text.save()
        news_text.news.is_parsed = True
        news_text.news.save()


class NewsTextParser(multiproc.MultiProc):
    """
    Extract all links from news text
    """

    task_manager = NewsText.objects.filter(is_parsed=False).iterator

    @staticmethod
    def worker(news_text: NewsText):
        url_list = [url for url in aParser.get_a_from_news_text(news_url=news_text.news.url, text=news_text.text)]
        return news_text, url_list

    @staticmethod
    def writer(container):
        news_text_obj, url_list = container
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


class AsyncTextPreparer(multiproc.MultiProc):
    task_manager = NewsText.objects.iterator

    @staticmethod
    def writer(write_obj):
        news_text, refined_text = write_obj
        news_text.text = refined_text
        news_text.save()

    @staticmethod
    def worker(news_text):
        try:
            print(news_text.pk)
            text = news_text.text
            refined_text = text_prerparer.text_preparer(text)
            return news_text, refined_text
        except:
            print(news_text)


def main():
    HtmlParser().run()
    NewsTextParser().run()
    AsyncTextPreparer().run()

if __name__ == "__main__":
    main()
