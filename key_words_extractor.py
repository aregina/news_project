import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news_project.settings")
django.setup()

from db.models import KeyWord, News
from prjparser import key_words


# TODO добавить проверку наличия newstext.text. Ломается при отсутсвии
def key_words_create():
    for news in News.objects.iterator():
        # Создать отдельный флаг для полей где уже были выделены ключи
        if news.keyword_set.exists():
            continue
        key_word_list = key_words.get_key_word(news.newstext.text, news.title)
        print(key_word_list)
        for word in key_word_list:
            try:
                key_word = KeyWord.objects.get(word=word)
            except:
                key_word = KeyWord(word=word)
                key_word.save()
            key_word.news.add(news)


def make_query(keys_list):
    q = News.objects
    for key in keys_list:
        q = q.filter(keyword__word=key)
    return q


if __name__ == "__main__":
    key_words_create()
