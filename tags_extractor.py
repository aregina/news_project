import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news_project.settings")
django.setup()

from db.models import NewsTags, News
from prjparser import news_tags


def tags_create():
    # тут лучше итерировать сразу NewsText
    # можно в модель NewsText добавить булево поле (признак того что ты этот текст уже посмотрел)
    # и сразу брать только непросмотренные тексты
    #   NewsText.objects.filter(___=False).iterator():
    for news in News.objects.iterator():
        tags_list = news_tags.get_tags(news.newstext.text)
        for tag in tags_list:
            # тут нужно истользовать только один метод создания записи в базе
            # или  nt = NewsTags(..)
            #       nt.save()
            # или NewsTags.objects.create()
            news_tag = NewsTags.objects.create(news=news, weight=tag[0], tag=tag[1])
            news_tag.save()


if __name__ == "__main__":
    tags_create()
