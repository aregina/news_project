from utils import DjangoSetup
from prjparser import multiproc, key_words
from db.models import News, KeyWord


class KeyWordsExtractor(multiproc.MultiProc):
    def worker(self, work_obj):
        news_pk, news_title, news_text = work_obj
        key_word_list = key_words.get_key_word(news_text, news_title)
        print("news_id {}\t num of keywords {}".format(news_pk, len(key_word_list)))
        return news_pk, key_word_list

    def task_manager(self):
        for news in News.objects.iterator():
            if not news.keyword_set.exists():
                yield news.pk, news.title, news.newstext.text

    def writer(self, write_obj):
        news_pk, key_word_list = write_obj
        for word in key_word_list:
            try:
                key_word = KeyWord.objects.get(word=word)
            except KeyWord.DoesNotExist:
                key_word = KeyWord(word=word)
                key_word.save()
            news = News.objects.get(pk=news_pk)
            key_word.news.add(news)


def main():
    KeyWordsExtractor().run()


if __name__ == "__main__":
    main()
