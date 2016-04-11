import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news_project.settings")
django.setup()

from db.models import News

for news in News.objects.iterator():
    if hasattr(news, 'newstext'):
        news.is_parsed = True
        news.save()
