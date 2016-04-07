import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news_project.settings")
django.setup()

from db.models import NewsTags, News
from prjparser import news_tags


def tags_create():
    for news in NewsText.objects.filter(check_tag=False).iterator():
        tags_list = news_tags.get_tags(news.newstext.text)
        for tag in tags_list:
            try:
                tag_id = AllTags.objects.get(tag=tag[1])
                NewsTags.objects.create(news=news, weight=tag[0], tag=tag_id)
            except:
                tag_id = AllTags.objects.create(tag=tag[1])
                NewsTags.objects.create(news=news, weight=tag[0], tag=tag_id)
                
        news.check_tag = True
        news.save()


if __name__ == "__main__":
    tags_create()
