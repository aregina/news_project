import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news_project.settings")
django.setup()
from db.models import News, NewsText
from django.db import transaction

with transaction.atomic():
    for newstext in NewsText.objects.iterator():
        if newstext.news.keyword_set.exists():
            newstext.is_keywords_extracted = True
            print("news id \t {}".format(newstext.news.pk))
            newstext.save()

