from utils import DjangoSetup
from prjparser import multiproc, vectorizer
from db.models import NewsText, NewsVector


class NewsVectorizer(multiproc.MultiProc):
    task_manager = NewsText.objects.filter(is_vectorized=False).iterator

    @staticmethod
    def worker(news_text: NewsText):
        print(news_text.pk)
        pickled_vector = vectorizer.get_pickled_vector(news_text.text)
        news_vector = NewsVector(news=news_text.news, vector=pickled_vector)
        return news_vector, news_text

    @staticmethod
    def writer(container):
        news_vector, news_text = container
        news_vector.save()
        news_text.is_vectorized = True
        news_text.save()


def main():
    import time
    start = time.time()
    NewsVectorizer(2).run()
    print("end time {}".format(time.time() - start))

if __name__ == "__main__":
    main()
