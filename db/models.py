from django.db import models


class Site(models.Model):
    name = models.CharField(max_length=100)


class News(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    url = models.URLField(max_length=300)
    pub_date = models.DateTimeField('date published')
    summary = models.TextField(blank=True, null=True)


class RssChannels(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    url = models.URLField(max_length=300)


class NewsText(models.Model):
    news = models.OneToOneField(
        News,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    text = models.TextField()


class KeyWord(models.Model):
    news = models.ManyToManyField(
            News)
    word = models.CharField(max_length=300)
