import pymorphy2

MORPH = pymorphy2.MorphAnalyzer()
PUNCTUATION_SIMBOLS = '!"#$%&\'()*+,./:;<=>?@[\\]^_`{|}~«»„'
WHITE_SPACES = ' ' * len(PUNCTUATION_SIMBOLS)


def get_plain_text(text, interesting_speach_parts):
    translate_dict = str.maketrans(PUNCTUATION_SIMBOLS, WHITE_SPACES)
    text_without_punctuation = text.translate(translate_dict)
    separated_words = text_without_punctuation.split()

    interesting_words_from_news = []
    for word in separated_words:
        parsed_word = MORPH.parse(word)[0]
        if parsed_word.tag.POS is None or parsed_word.tag.POS in interesting_speach_parts:
            interesting_words_from_news.append(parsed_word.normal_form)

    plain_text = ' '.join(interesting_words_from_news)

    return plain_text


def get_plain_words_list(text, interesting_speach_parts):
    separated_words = text.split()

    plain_words_list = []
    for word in separated_words:
        parsed_word = MORPH.parse(word)[0]
        if parsed_word != '-' and parsed_word.tag.POS in interesting_speach_parts:
            plain_words_list.append(parsed_word.normal_form)

    return plain_words_list


def text_preparer(text):
    interestig_speach_parts = {
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
        'UNKN',
    }
    final_text = get_plain_text(text, interestig_speach_parts)
    return final_text


def get_only_noun(text):
    interestig_speach_parts = {
        'NOUN',
    }
    final_word_list = get_plain_words_list(text, interestig_speach_parts)
    return final_word_list
