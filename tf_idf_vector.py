from utils import DjangoSetup
from sklearn.feature_extraction.text import TfidfVectorizer
from db.models import NewsText, News, NewsVector
from scipy.spatial.distance import cosine
import pickle


def get_text(news_text_id):
    try:
        text = NewsText.objects.get(pk=news_text_id).text
    except:
        text = None
    return text


def print_news_title(news_text_id):
    title = NewsText.objects.get(pk=news_text_id).news.title
    print("\t{}\t{}".format(title, news_text_id))


def compare_news(id1, id2, vectorizer):
    n1 = vectorizer.transform([get_text(id1)])
    n2 = vectorizer.transform([get_text(id2)])
    return cosine(n1.toarray(), n2.toarray())


def compare_news_vector(first_news_vector, second_news_vector):
    return cosine(first_news_vector.toarray(), second_news_vector.toarray())


def get_tf_idf(big_text):
    tf_idf = TfidfVectorizer(min_df=1)
    tf_idf.fit(big_text.split())
    return tf_idf


def get_big_text():
    text_array = [news_text.text for news_text in NewsText.objects.all()]
    big_text = " ".join(text_array)
    return big_text


def main():
    big_text = get_big_text()
    tf_idf = get_tf_idf(big_text)

    for news_text in NewsText.objects.iterator():
        if hasattr(news_text.news, "newsvector"):
            continue
        print(news_text.pk)
        vector = tf_idf.transform([news_text.text])
        pickled_vector = pickle.dumps(vector)
        NewsVector.objects.create(news=news_text.news, vector=pickled_vector)


def write_vector():
    big_text = get_big_text()
    tf_idf = get_tf_idf(big_text)

    news_text = get_text(51465)
    news_vector = tf_idf.transform([news_text])
    return news_vector


def news_comparer(news_id):
    news = News.objects.get(pk=news_id)
    news_v = pickle.loads(news.newsvector.vector)
    print(news.title)
    for n in News.objects.iterator():
        n_v = pickle.loads(n.newsvector.vector)
        if not n_v.getnnz():
            continue
        text_similarity = compare_news_vector(news_v, n_v)
        if text_similarity < 0.7:
            print(text_similarity, end="\t")
            print(n.title)


if __name__ == "__main__":
    # main()
    news_comparer(50)
