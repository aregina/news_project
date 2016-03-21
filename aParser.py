import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news_project.settings")
django.setup()

from prjparser import urlOpen, textParser
import html
import re


test_url = "https://meduza.io/"

txt = urlOpen.read(test_url)
txt = html.unescape(txt)


def a_gen(text):
    end = 0
    while end < len(text):
        y = re.search("<a(.|\s)*?</a>", text[end:])
        if not y:
            break
        else:
            yield y.group()
            end += y.end()


def a_print(text):
    """TODO: looks like textParser.S
    :param text:
    """
    text = text[re.search("</\s*?head\s*?>", text).end():]

    for link in a_gen(text):
        print(link)
        f = re.search("href=\"(.*?)\"", link)
        if not f:
            continue
        url = f.group(1)
        if not url.startswith("http"):
            print("bad")
        words = re.sub("<(.|\s)*?>", " ", link).split()
        len_w = len(words)
        if len_w > 0:
            print("{} {} {}\n".format(url, " ".join(words), len_w))


a_print(txt)
