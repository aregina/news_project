from utils import DjangoSetup
from prjparser import multiproc, key_words
from db.models import News, KeyWord, NewsText


class KeyWordsExtractor(multiproc.MultiProc):
    @staticmethod
    def worker(work_obj):
        news_pk, news_title, news_text = work_obj
        key_word_list = key_words.get_key_word(news_text, news_title)
        print("news_id {}\t num of keywords {}".format(news_pk, len(key_word_list)))
        return news_pk, key_word_list

    @staticmethod
    def task_manager():
        for news_text in NewsText.objects.filter(is_keywords_extracted=False).iterator():
            yield news_text.news.pk, news_text.news.title, news_text.text

    @staticmethod
    def writer(write_obj):
        news_pk, key_word_list = write_obj
        news = News.objects.get(pk=news_pk)
        print("pk {} write".format(news_pk))
        for word in key_word_list:
            try:
                key_word = KeyWord.objects.get(word=word)
            except KeyWord.DoesNotExist:
                key_word = KeyWord(word=word)
                key_word.save()
            key_word.news.add(news)
        news.newstext.is_keywords_extracted = True
        news.newstext.save()


class KeyWordsExtractorMySql(multiproc.MultiProc):
    @staticmethod
    def worker(news_text):
        key_word_list = key_words.get_key_word(news_text.text, news_text.news.title)
        for word in key_word_list:
            key_word, is_created = KeyWord.objects.get_or_create(word=word)
            key_word.news.add(news_text.news)
        news_text.is_keywords_extracted = True
        news_text.save()
        return news_text.pk, len(key_word_list)

    @staticmethod
    def task_manager():
        for news_text in NewsText.objects.filter(is_keywords_extracted=False).iterator():
            yield news_text

    @staticmethod
    def writer(write_obj):
        pk, num_keywords = write_obj
        print("news_id {}\t num of keywords {}".format(pk, num_keywords))


def time_it(func):
    import time

    def warp():
        start = time.time()
        func()
        print(time.time() - start)

    return warp


@time_it
def main():
    KeyWordsExtractorMySql().run()


if __name__ == "__main__":
    main()
