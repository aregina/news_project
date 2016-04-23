import pymorphy2

MORPH = pymorphy2.MorphAnalyzer()
PUNCTUATION_SIMBOLS = '!"#$%&\'()*+,./:;<=>?@[\\]^_`{|}~'
WHITE_SPACES = ' ' * len(PUNCTUATION_SIMBOLS)
INTERESTING_SPEACH_PARTS = {
    'NOUN',
    'ADJF',
    'ADJS',
    'VERB',
    'NUMR',
    'ADVB',
    'COMP',
    'INFN',
    'PRTF',
    'PRTS',
    'GRND',
}


def text_preparer(text):
    translate_dict = str.maketrans(PUNCTUATION_SIMBOLS, WHITE_SPACES)
    text_without_punctuation = text.translate(translate_dict)
    separated_words = text_without_punctuation.split()

    interesting_words_from_news = []
    for word in separated_words:
        parsed_word = MORPH.parse(word)[0]

        if parsed_word.tag.POS is None or parsed_word.tag.POS in INTERESTING_SPEACH_PARTS:
            interesting_words_from_news.append(parsed_word.normal_form)

    plain_text = ' '.join(interesting_words_from_news)

    return plain_text
