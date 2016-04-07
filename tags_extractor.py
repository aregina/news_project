import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news_project.settings")
django.setup()

from db.models import NewsTags, NewsText, AllTags
from prjparser import news_tags


def tags_create():

    for news_text in NewsText.objects.filter(check_tag=False).iterator():
        tags_list = news_tags.get_tags(news_text.text)
        for tag in tags_list:
            try:
                tag_from_db = AllTags.objects.get(tag=tag[1])
            except AllTags.DoesNotExist:
                tag_from_db = AllTags.objects.create(tag=tag[1])
            tag_id = tag_from_db.id
            NewsTags.objects.create(news=news_text, weight=tag[0], tag=tag_id)
                
        news.check_tag = True
        news.save()


if __name__ == "__main__":
    tags_create()
