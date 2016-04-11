import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news_project.settings")
django.setup()

from db.models import NewsTags, NewsText, AllTags
from prjparser import news_tags


def tags_create():
    for news_text in NewsText.objects.filter(check_tag=False).iterator():
        tags_list = news_tags.get_tags(news_text.text)
        for tag in tags_list:
            for weight, tag_text in tag:
                try:
                    tag_from_db = AllTags.objects.get(tag=tag_text)
                except AllTags.DoesNotExist:
                    tag_from_db = AllTags.objects.create(tag=tag_text)
                print(weight, tag_from_db)
                NewsTags.objects.create(news=news_text, weight=weight, tag=tag_from_db)

        news_text.news.check_tag = True
        news_text.news.save()

if __name__ == "__main__":
    tags_create()


