from db.models import KeyWord, NewsText, News

def themes(date):
    key_words = []

    for news in News.objects.filter(pub_date=date).iterator():
        news.

