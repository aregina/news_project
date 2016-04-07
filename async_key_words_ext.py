from utils import DjangoSetup
from prjparser import multiproc, key_words
from db.models import News, KeyWord


class KeyWordsExtractor(multiproc.MultiProc):
    def worker(self, news):
        key_word_list = key_words.get_key_word(news.newstext.text, news.title)
        return news, key_word_list

    def task_manager(self):
        for news in News.objects.iterator():
            if not news.keyword_set.exists():
                yield news

    def writer(self, write_obj):
        news = write_obj[0]
        key_word_list = write_obj[1]
        for word in key_word_list:
            try:
                key_word = KeyWord.objects.get(word=word)
            except:
                key_word = KeyWord(word=word)
                key_word.save()
            key_word.news.add(news)
