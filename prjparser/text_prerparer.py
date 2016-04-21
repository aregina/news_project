import pymorphy2
import string

MORPH = pymorphy2.MorphAnalyzer()
PUNCTUATION_SIMBOLS = string.punctuation
WHITE_SPASES = ' ' * len(PUNCTUATION_SIMBOLS)
INTERESTING_SPEACH_PARTS = ['NOUN', 'ADJF', 'ADJS', 'VERB', 'NUMR', 'ADVB']


def text_prerarer(text):
    text_without_punctuation = str.maketrans(PUNCTUATION_SIMBOLS, WHITE_SPASES)
    separeted_words = text_without_punctuation.split()
    interesting_words_from_news = []
    for speech_parts in INTERESTING_SPEACH_PARTS:
        for word in separeted_words:
            parsed_word = MORPH.parse(word)[0]
            if speech_parts in parsed_word.tag:
                interesting_words_from_news.append(parsed_word.normal_form)
    return interesting_words_from_news


