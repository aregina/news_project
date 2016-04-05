import os, django
 
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news_project.settings")
django.setup()
 
from db.models import NewsTags, News
from prjparser import news_tags
 


def tags_create():
    for news in News.objects.iterator():
        tags_list = news_tags.get_tags(news.newstext.text)
        print(tags_list)
        for tag in tags_list:
            try:
                tag = NewsTags.objects.get(tag=tags_list[0],)
            except:
                tag = NewsTags.objects.create(tag=tags_list[0])
                tag.save()
            tag.news.add(news)


if __name__ == "__main__":
    tags_create()