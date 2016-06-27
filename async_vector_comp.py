from utils import DjangoSetup
from prjparser import multiproc, vectorizer
from db.models import News, NewsVector


class NewsComparer(multiproc.MultiProc):
    @staticmethod
    def task_manager():
        pass

    @staticmethod
    def worker(parse_obj):
        pass

    @staticmethod
    def writer(write_obj):
        pass
