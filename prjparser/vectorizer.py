from utils import DjangoSetup
from sklearn.feature_extraction.text import TfidfVectorizer
from db.models import NewsText, News, NewsVector
from scipy.spatial.distance import cosine
import pickle
import numpy
from scipy.sparse import csr_matrix

FILE_PATH = "prjparser/tf_idf_vectorizer.bin"


def get_time(func):
    import time

    def warp(*args):
        start = time.time()
        res = func(*args)
        print(time.time() - start)
        return res

    return warp


def compare_news_vector(first_news_vector, second_news_vector):
    return cosine(first_news_vector, second_news_vector)


def get_tf_idf(big_text):
    tf_idf = TfidfVectorizer(min_df=1)
    tf_idf.fit(big_text.split())
    return tf_idf


def get_big_text():
    text_array = [news_text.text for news_text in NewsText.objects.all()]
    big_text = " ".join(text_array)
    return big_text


def news_comparer(news_id):
    pivot_news = News.objects.get(pk=news_id)
    pivot_news_vector = pickle.loads(pivot_news.newsvector.vector)
    pivot_news_arr = pivot_news_vector.toarray()[0]
    # print(pivot_news.title)
    # count = 0
    for news_vector in NewsVector.objects.all():
        vector = pickle.loads(news_vector.vector)
        # if not vector.getnnz():
        #     continue
        # print(news_vector.news.pk, end="\n")
        text_similarity = compare_news_vector_with_(pivot_news_arr, vector)[0]
        # text_similarity2 = compare_news_vector(pivot_news_arr, vector.toarray()[0])
        # if text_similarity2 != text_similarity and (text_similarity - text_similarity2) > 0.000001:
        #     print(news_vector.pk)
        if text_similarity < 0.71:
            # count += 1
            news_vector.news.related_news.add(pivot_news)
            # print(text_similarity, end="\t")
            # print(news_vector.news.pk, end="\t")
            # print(news_vector.news.title)
            # print(count)


def get_pickled_vector(text):
    vector = tf_idf_var.transform([text])
    return pickle.dumps(vector)


def make_tf_idf_file():
    big_text = get_big_text()
    tf_idf = get_tf_idf(big_text)
    with open(FILE_PATH, "wb") as file:
        file.write(pickle.dumps(tf_idf))


def open_tf_idf_file():
    f = open(FILE_PATH, "rb").read()
    return pickle.loads(f)


@get_time
def compare_news_vector_with_to_array(first_news_vector, second_news_vector):
    return cosine(first_news_vector.toarray(), second_news_vector.toarray())


# @get_time
def compare_news_vector_with_(arr, vec: csr_matrix):
    return 1 - vec.dot(arr)


# @get_time
def compare_news_vector_with_1(arr, vec: csr_matrix):
    return 1 - vec._mul_vector(arr)


def comp_all_news(start=0):
    a = NewsVector.objects.all()
    for i in range(start, len(a) - 1):
        print(i)
        pivot_news_vector = pickle.loads(a[i].vector)
        if pivot_news_vector.getnnz() == 0:
            continue
        pivot_news_arr = pivot_news_vector.toarray()[0]
        for j in range(i, len(a)):
            vector = pickle.loads(a[j].vector)
            text_similarity = compare_news_vector_with_(pivot_news_arr, vector)[0]
            if text_similarity < 0.71:
                a[j].news.related_news.add(a[i].news)


@get_time
def main():
    # news_comparer(29)
    comp_all_news()
    # v = NewsVector.objects.get(pk=1605)
    # v1 = NewsVector.objects.get(pk=1600)
    #
    # pic_v = pickle.loads(v.vector)
    # arr_pic_v = pic_v.toarray()[0]
    # piv_v1 = pickle.loads(v1.vector)
    # print(compare_news_vector(pic_v.toarray(), piv_v1.toarray()))
    # print(compare_news_vector_with_to_array(pic_v, piv_v1))
    # print(compare_news_vector_with_(arr_pic_v,piv_v1)[0])
    # print(compare_news_vector_with_1(arr_pic_v,piv_v1)[0])
    # print(arr_pic_v.__class__)


if __name__ == "__main__":
    main()
else:
    import os.path

    if not os.path.isfile(FILE_PATH):
        make_tf_idf_file()
    tf_idf_var = open_tf_idf_file()
