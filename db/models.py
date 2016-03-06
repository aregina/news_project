from django.db import models


class Site(models.Model):
    site_name = models.CharField(max_length=100)


class News(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    url = models.CharField(max_length=300)
    pub_date = models.DateTimeField('date published')
    summary = models.TextField(blank=True, null=True)


class RssChannels(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    url = models.CharField(max_length=300)
