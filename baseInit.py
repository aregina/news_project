import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news_project.settings")
django.setup()

from db.models import Site, RssChannels, ASources

# TODO выделить в отдельный файл м.б. json
news_dict = {"lenta.ru": ["http://www.lenta.ru/rss", ],
             "tass.ru": ["http://tass.ru/rss/v2.xml"],
             "rbc.ru": ["http://static.feed.rbc.ru/rbc/internal/rss.rbc.ru/rbc.ru/mainnews.rss"],
             "interfax.ru": ["http://www.interfax.ru/rss.asp"],
             "regnum.ru": ["http://regnum.ru/rss/main"],
             "newsru.com": ["http://feeds.newsru.com/com/www/news/main"],
             "rosbalt.ru": ["http://www.rosbalt.ru/feed/"],
             "ria.ru": ["http://ria.ru/export/rss2/economy/index.xml", "http://ria.ru/export/rss2/world/index.xml",
                        "http://ria.ru/export/rss2/politics/index.xml"],
             "meduza.io": ["https://meduza.io/rss/all"], }

link_dict = {'lenta.ru': "http://lenta.ru/",
             "rbc.ru": "http://www.rbc.ru/"}


def get_site(name):
    site = Site.objects.filter(name=name)[:1]
    if not site.exists():
        return Site.objects.create(name=name)
    else:
        return site[0]


def rss_create(site, rss_list):
    for rss in rss_list:
        channel = RssChannels.objects.filter(url=rss)[:1]
        if not channel.exists():
            RssChannels.objects.create(site=site, url=rss)


def a_create(site, link):
    if not ASources.objects.filter(url=link).exists():
        ASources.objects.create(site=site, url=link)


def make_database_entry(source_dict, entry_type):
    for site_name in source_dict.keys():
        s = get_site(site_name)
        if entry_type == "rss":
            rss_create(s, source_dict[site_name])
        elif entry_type == "a":
            a_create(s, source_dict[site_name])
        else:
            raise TypeError


# TODO не разделять на два странных метода
def main():
    make_database_entry(news_dict, "rss")
    make_database_entry(link_dict, "a")


if __name__ == "__main__":
    main()
