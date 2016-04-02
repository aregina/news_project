from prjparser import urlOpen, textParser
import re


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

    href = re.search("href=\"(.*?)\"", a_tag)
    if not href:
        return
    return href.group(1)

    # urlparse = urllib.parse.urlparse(url)
    # scheme, netloc, path = urlparse[0:3]
    # url = "{}//{}{}".format(scheme, netloc, path)


def get_url_and_url_text(html_code, site_address):
    """TODO: looks like textParser.S
    :param site_address:
    :param html_code:
    """
    import urllib.parse
    for a in get_a(html_code):
        url = get_url_or_none(a)
        if not url:
            continue
        if url.startswith('/'):
            url = urllib.parse.urljoin(site_address, url[1:])
        if not url.startswith("http"):
            continue

        words = re.sub("<(.|\s)*?>", " ", a).split()
        len_w = len(words)
        if len_w > 4:
            yield url, " ".join(words)


def main():
    test_url = "http://gazeta.ru/"
    txt = urlOpen.get_html(test_url)
    txt = textParser.tags_filter_head_and_script(txt)
    for url, text in get_url_and_url_text(txt):
        if url.startswith(test_url):
            print("{} {}\n".format(url, text))


if __name__ == "__main__":
    main()
