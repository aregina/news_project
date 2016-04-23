from utils import DjangoSetup

from prjparser import text_prerparer, multiproc
from db.models import NewsText


class AsyncTextPreparer(multiproc.MultiProc):
    task_manager = NewsText.objects.iterator

    def writer(self, write_obj):
        news_text, refined_text = write_obj
        news_text.text = refined_text
        news_text.save()

    def worker(self, news_text):
        try:
            text = news_text.text
            refined_text = text_prerparer.text_preparer(text)
            return news_text, refined_text
        except:
            print(news_text)


def main():
    # news_text = NewsText.objects.get(pk=49000)
    #
    # text = news_text.text
    # print(text)
    # text = text_prerparer.text_preparer(text)
    # print(text)
    AsyncTextPreparer().run()


if __name__ == "__main__":
    main()
