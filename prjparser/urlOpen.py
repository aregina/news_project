import urllib.request as u
import urllib.error


def get_html(url):
    try:
        with u.urlopen(url) as request:
            html_code = request.read()
            if request.getheader('Content-Encoding') == 'gzip':
                import gzip
                html_code = gzip.decompress(html_code)
    except urllib.error.HTTPError as e:
        print("HTTPError {}".format(e.msg))
        return None
    except urllib.error.URLError as e:
        print("URLError {}".format(e.reason))
        return None
    encodings = ["utf8", "cp1251"]
    for encode in encodings:
        try:
            html_code = html_code.decode(encoding=encode)
        except UnicodeDecodeError:
            continue
        else:
            return html_code
