import urllib.request as u


def get_html(url):
    with u.urlopen(url) as request:
        html_code = request.read()
        if request.getheader('Content-Encoding') == 'gzip':
            import gzip
            html_code = gzip.decompress(html_code)

    encodings = ["utf8", "cp1251"]
    for encode in encodings:
        try:
            html_code = html_code.decode(encoding=encode)
        except UnicodeDecodeError:
            print("error")
            continue
        else:
            return html_code
