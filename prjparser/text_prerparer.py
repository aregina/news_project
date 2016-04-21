import string

import pymorphy2
from textblob import TextBlob

MORPH = pymorphy2.MorphAnalyzer()
PUNCTUATION_SIMBOLS = string.punctuation
WHITE_SPASES = ' ' * len(PUNCTUATION_SIMBOLS)
INTERESTING_SPEACH_PARTS = ['NOUN', 'ADJF', 'ADJS', 'VERB', 'NUMR', 'ADVB']


def text_prerarer(text):
    text_without_punctuation = str.maketrans(PUNCTUATION_SIMBOLS, WHITE_SPASES)
    separated_words = text_without_punctuation.split()

    tb_news = TextBlob(separated_words)
    words_from_news = list(tb_news.words)

    interesting_words_from_news = []
    for speech_parts in INTERESTING_SPEACH_PARTS:
        for word in words_from_news:
            parsed_word = MORPH.parse(word)[0]
            if speech_parts in parsed_word.tag:
                interesting_words_from_news.append(parsed_word.normal_form)

    return interesting_words_from_news
