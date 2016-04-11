from django.db import models


class Site(models.Model):
    name = models.CharField(max_length=100)


class News(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    url = models.URLField(max_length=300, db_index=True)
    pub_date = models.DateTimeField('date published', db_index=True)
    summary = models.TextField(blank=True, null=True)
    is_parsed = models.BooleanField('text was parsed?', default=False)


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
    is_keywords_extracted = models.BooleanField(default=False)
    is_parsed = models.BooleanField(default=False)
    check_tag = models.BooleanField(default=False)



class KeyWord(models.Model):
    news = models.ManyToManyField(News)
    word = models.CharField(max_length=300)


class AllTags(models.Model):
    tag = models.CharField(max_length=20)


class NewsTags(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    tag = models.ForeignKey(AllTags, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=6, decimal_places=3)


class ASources(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    url = models.URLField(max_length=300)


class UrlInText(models.Model):
    news = models.ManyToManyField(
        News)
    url = models.URLField(max_length=300, db_index=True)
