from utils import DjangoSetup
from sklearn.feature_extraction.text import TfidfVectorizer
from db.models import NewsText
from scipy.spatial.distance import cosine


def get_text(id_news_text):
    try:
        text = NewsText.objects.get(pk=id_news_text).text
    except:
        text = "офшор"
    return text


def print_news_title(news_id):
    title = NewsText.objects.get(pk=news_id).news.title
    print("\t{}\t{}".format(title, news_id))


def compare_news(id1, id2, vectorizer):
    n1 = vectorizer.transform([get_text(id1)])
    n2 = vectorizer.transform([get_text(id2)])
    return cosine(n1.toarray(), n2.toarray())


def main():
    text_array = [news_text.text for news_text in NewsText.objects.all()]
    big_text = " ".join(text_array)

    tf_idf = TfidfVectorizer(min_df=1)
    tf_idf.fit(big_text.split())

    pivot_news_text_id = 51465
    print_news_title(pivot_news_text_id)
    for news_text in NewsText.objects.iterator():
        text_similarity = compare_news(pivot_news_text_id, news_text.pk, tf_idf)
        if text_similarity < 0.7:
            print(text_similarity)
            print_news_title(news_text.pk)


if __name__ == "__main__":
    main()
