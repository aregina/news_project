from utils import DjangoSetup
from prjparser import multiproc, vectorizer
from db.models import News, NewsVector
import pickle


class NewsComparer(multiproc.MultiProc):
    task_manager = NewsVector.objects.filter(is_compared=False)[:30].iterator

    @staticmethod
    def worker(parse_obj):
        pivot_news_vector = pickle.loads(parse_obj.vector)
        if pivot_news_vector.getnnz() == 0:
            return
        pivot_news_arr = pivot_news_vector.toarray()[0]
        simil_list = list()
        for vec in NewsVector.objects.filter(pk__lt=parse_obj.pk):
            vector = pickle.loads(vec.vector)
            text_similarity = vectorizer.compare_news_vector_with_(pivot_news_arr, vector)[0]
            if text_similarity < 0.71:
                simil_list.append(vec)
            simil_list.append(parse_obj)
        return simil_list

    @staticmethod
    def writer(write_obj):
        print(write_obj[~0].pk)
        for v in write_obj:
            write_obj[~0].news.related_news.add(v.news)
        write_obj[~0].is_compared = True
        write_obj[~0].save()


def main():
    NewsComparer().run()


if __name__ == "__main__":
    main()
