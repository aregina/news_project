import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news_project.settings")
django.setup()

from db.models import Site, RssChannels, ASources

news_dict = {"lenta.ru": ["http://www.lenta.ru/rss", ], "tass.ru": ["http://tass.ru/rss/v2.xml"],
             "rbc.ru": ["http://static.feed.rbc.ru/rbc/internal/rss.rbc.ru/rbc.ru/mainnews.rss"],
             "interfax.ru": ["http://www.interfax.ru/rss.asp"],
             "regnum.ru": ["http://regnum.ru/rss/main"], "newsru.com": ["http://feeds.newsru.com/com/www/news/main"],
             "rosbalt.ru": ["http://www.rosbalt.ru/feed/"],
             "ria.ru": ["http://ria.ru/export/rss2/economy/index.xml", "http://ria.ru/export/rss2/world/index.xml",
                        "http://ria.ru/export/rss2/politics/index.xml"],
             "meduza.io": ["https://meduza.io/rss/all"], }


def get_site(name):
    site = Site.objects.filter(name=name)[:1]
    if not site.exists():
        return Site.objects.create(name=name)
    else:
        return site[0]

for site_name in news_dict.keys():
    s = get_site(site_name)
    for rss in news_dict[site_name]:
        if not RssChannels.objects.filter(url=rss).exists():
            r = RssChannels(site=s, url=rss)
            r.save()

link_dict = {'lenta.ru': "http://lenta.ru/",
             "rbc.ru": "http://www.rbc.ru/"}

for site_name in link_dict.keys():
    s = get_site(site_name)
    link = link_dict[site_name]
    if not ASources.objects.filter(url=link).exists():
        ASources.objects.create(site=s, url=link)

