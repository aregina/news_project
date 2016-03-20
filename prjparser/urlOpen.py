import urllib.request as u


def read(url):
    with u.urlopen(url) as a:
        txt = a.read()
        if a.getheader('Content-Encoding') == 'gzip':
            import gzip
            txt = gzip.decompress(txt)

    encodings = ["utf8", "cp1251"]
    for encode in encodings:
        try:
            txt = txt.decode(encoding=encode)
        except UnicodeDecodeError:
            print("error")
            continue
        else:
            return txt
