"""
WSGI config for news_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""


import os, sys

sys.path.append('/usr/project/news_prj')

from django.core.wsgi import get_wsgi_application

os.environ['DJANGO_SETTINGS_MODULE'] = 'news_project.settings'

application = get_wsgi_application()
