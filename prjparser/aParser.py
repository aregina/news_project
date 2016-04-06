from prjparser import urlOpen, textParser,model
import re
import urllib.parse
from datetime import datetime


def get_a(text):
    end = 0
    while end < len(text):
        y = re.search("<a(.|\s)*?</a>", text[end:])
        if not y:
            return
        else:
            yield y.group()
            end += y.end()


def get_href_from_a_or_none(a_tag):
    href = re.search("href=\"(.*?)\"", a_tag)
    if not href:
        return
    return href.group(1)


def remove_query_from_url(url):
    urlparse = urllib.parse.urlparse(url)
    scheme, netloc, path = urlparse[0:3]
    url = "{}://{}{}".format(scheme, netloc, path)
    return url


def normolize_url(url, news_url):
    if not url:
        return
    if url.startswith('/'):
        scheme, netloc = urllib.parse.urlparse(news_url)[0:2]
        site_url = "{}://{}".format(scheme, netloc)
        url = urllib.parse.urljoin(site_url, url[1:])
    if not url.startswith('http'):
        return
    url = remove_query_from_url(url)
    return url


def get_a_from_news_text(news_url, text):
    for a in get_a(text):
        url = get_href_from_a_or_none(a)
        url = normolize_url(url, news_url)
        if url:
            yield url


def remove_all_tags(text):
    return re.sub("<(.|\s)*?>", " ", text)


def get_url_and_url_text(html_code, site_address):
    """TODO: looks like textParser.S
    :param site_address:
    :param html_code:
    """
    for a in get_a(html_code):
        url = get_href_from_a_or_none(a)
        url = normolize_url(url, site_address)
        if not url or not url.startswith(site_address):
            continue

        # Считаем количество слов в ссылке и убираем лишние пробелы
        words = remove_all_tags(a).split()
        len_w = len(words)
        # ссылки с количеством слов меньше 4 не ведут на новость
        if len_w > 4:
            yield url, " ".join(words)


def parse(source_url: str):
    html_code = urlOpen.get_html(source_url)
    html_code = textParser.tags_filter_head_and_script(html_code)
    for url, text in get_url_and_url_text(html_code, source_url):
        yield model.NewsData(url=url,
                             title=text,
                             pub_date=datetime.now(),
                             summary=None)


def main():
    test_url = "http://gazeta.ru/"
    txt = urlOpen.get_html(test_url)
    txt = textParser.tags_filter_head_and_script(txt)
    for url, text in get_url_and_url_text(txt, test_url):
        if url.startswith(test_url):
            print("{} {}\n".format(url, text))


if __name__ == "__main__":
    main()
