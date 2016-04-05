import os, django
 
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news_project.settings")
django.setup()
 
from db.models import NewsTags, News
from prjparser import news_tags
 


def tags_create():
    for news in News.objects.iterator():
        tags_list = news_tags.get_tags(news.newstext.text)
        print(tags_list)
        for v in tags_list:
        try:
                tag1 = NewsTags.objects.get(tag=tags_list[0],)
                #tag2 = NewsTags.objects.get(tag=tags_list[1])
                #tag3 = NewsTags.objects.get(tag=tags_list[2])
        except:
                tag1 = NewsTags.objects.create(tag1=tags_list[0])
                #tag2 = NewsTags(tag2=tags_list[1])
                #tag3 = NewsTags(tag3=tags_list[2])
                # tag1.save()
                # tag2.save()
                # tag3.save()
        tag1.news.add(news)
        # tag2.news.add(news)
        # tag3.news.add(news)





if __name__ == "__main__":
    tags_create()