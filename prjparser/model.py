class NewsData:
    def __init__(self, url, title, pub_date, site_obj=None, summary=None):
        self.url = url
        self.title = title
        self.pub_date = pub_date
        self.summary = summary
        self.site_obj = site_obj
