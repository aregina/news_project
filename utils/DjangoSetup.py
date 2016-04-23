import django
import os

# os.chdir("..")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news_project.settings")
django.setup()
