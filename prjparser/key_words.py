from collections import Counter
from prjparser.text_prerparer import get_only_noun, text_preparer


def get_key_word(news, news_title):
    plain_news_title = text_preparer(news_title)
    interesting_words_from_news = get_only_noun(news)
    interesting_words_from_title = get_only_noun(plain_news_title)
    all_interesting_words = interesting_words_from_news + interesting_words_from_title
    counted_words = Counter(all_interesting_words)

    for word in interesting_words_from_title:
        if word in counted_words:
            counted_words[word] *= 3

    key_words_count = 10
    all_words = counted_words.most_common(key_words_count)

    with open('anti_key_words.txt') as anti_key_words_file:
        anti_key_words = set(anti_key_words_file.read().splitlines())

    key_words = []
    for word in all_words:
        if word[0] not in anti_key_words:
            key_words.append(word[0])

    return key_words
