import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news_project.settings")
django.setup()

from prjparser import urlOpen, textParser
import html

test_url = "http://news.rambler.ru/"

txt = urlOpen.read(test_url)
txt = html.unescape(txt)


def a_print(text):
    """TODO: looks like textParser.S
    :param text:
    """
    import re
    text = text[re.search("</\s*?head\s*?>", text).end():]
    end = 0
    while end < len(text):
        y = re.search("<a(.|\s)*?</a>", text[end:])
        if not y:
            break
        else:
            end += y.end()
            sub = y.group()
            f = re.search("href=\"(.*?)\"", sub)
            if not f:
                continue
            url = f.group(1)
            if not url.startswith("http"):
                if url.startswith('/'):
                    url = test_url+url[1:]
                else:
                    print("bad")
            words = re.sub("<(.|\s)*?>", " ", sub).split()
            len_w = len(words)
            if len_w > 0:
                print("{} {} {}\n".format(url, " ".join(words), len_w))


a_print(txt)
