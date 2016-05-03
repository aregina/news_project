from utils import DjangoSetup

from prjparser import text_prerparer, multiproc
from db.models import NewsText


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
    AsyncTextPreparer().run()


if __name__ == "__main__":
    main()
