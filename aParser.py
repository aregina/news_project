from prjparser import urlOpen, textParser
import re

import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news_project.settings")
django.setup()


def get_a(text):
    end = 0
    while end < len(text):
        y = re.search("<a(.|\s)*?</a>", text[end:])
        if not y:
            return
        else:
            yield y.group()
            end += y.end()


def get_url_or_none(a_tag):
    import urllib.parse
    href = re.search("href=\"(.*?)\"", a_tag)
    if not href:
        return
    url = href.group(1)
    if url.startswith('/'):
        url = urllib.parse.urljoin(test_url, url[1:])
    if url.startswith("http"):
        return url


def get_url_and_url_text(html_code):
    """TODO: looks like textParser.S
    :param html_code:
    """
    for a in get_a(html_code):
        url = get_url_or_none(a)
        if not url:
            continue

        words = re.sub("<(.|\s)*?>", " ", a).split()
        len_w = len(words)
        if len_w > 4:
            yield url, " ".join(words)


test_url = "http://ria.ru/"
txt = urlOpen.get_html(test_url)
txt = textParser.tags_filter_head_and_script(txt)
for url, text in get_url_and_url_text(txt):
    print("{} {}\n".format(url, text))
