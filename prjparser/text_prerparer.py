import string

import pymorphy2
from textblob import TextBlob

MORPH = pymorphy2.MorphAnalyzer()
PUNCTUATION_SIMBOLS = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
WHITE_SPACES = ' ' * len(PUNCTUATION_SIMBOLS)
INTERESTING_SPEACH_PARTS = ['NOUN', 'ADJF', 'ADJS', 'VERB', 'NUMR', 'ADVB']


def text_preparer(text):
    text_without_punctuation = text.maketrans(PUNCTUATION_SIMBOLS, WHITE_SPACES)
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
