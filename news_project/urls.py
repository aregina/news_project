"""news_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
import db.views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', db.views.index, name='index'),
    url(r'^tags/$', db.views.tags, name='tags'),
    url(r'^tags/daily$', db.views.tags, {'daily': True},name='tags'),
    url(r'^tags/(?P<tag>(\w|\+)+)/$', db.views.tag_detail, name='tag_detail'),
    url(r'^news/id(?P<news_id>[0-9]+)/$', db.views.news_detail, name='tag_detail'),
]
