from utils import DjangoSetup
from sklearn.feature_extraction.text import TfidfVectorizer
from db.models import NewsText
from scipy.spatial.distance import cosine


def get_text(news_text_id):
    try:
        text = NewsText.objects.get(pk=news_text_id).text
    except:
        text = "офшор"
    return text


def print_news_title(news_text_id):
    title = NewsText.objects.get(pk=news_text_id).news.title
    print("\t{}\t{}".format(title, news_text_id))


def compare_news(id1, id2, vectorizer):
    n1 = vectorizer.transform([get_text(id1)])
    n2 = vectorizer.transform([get_text(id2)])
    return cosine(n1.toarray(), n2.toarray())


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

    pivot_news_text_id = 51465
    print_news_title(pivot_news_text_id)
    for news_text in NewsText.objects.iterator():
        text_similarity = compare_news(pivot_news_text_id, news_text.pk, tf_idf)
        if text_similarity < 0.7:
            print(text_similarity)
            print_news_title(news_text.pk)


def write_vector():
    big_text = get_big_text()
    tf_idf = get_tf_idf(big_text)

    news_text = get_text(51465)
    news_vector = tf_idf.transform([news_text])
    with open("vector.txt", "w") as f:
        f.write(news_vector.toarray())


if __name__ == "__main__":
    write_vector()
