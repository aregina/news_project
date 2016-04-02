import pymorphy2
from collections import Counter
morph = pymorphy2.MorphAnalyzer()


def get_key_word(news, news_title):
    special_characters = '.,!()-"":;?«»'
    for character in special_characters:
        news = news.replace(character, ' ')
        news_title = news_title.replace(character, ' ')

    words_from_news = news.split()
    words_from_title = news_title.split()

    #interesting_speach_parts = ['NOUN', 'ADJF', 'ADJS', 'VERB', 'NUMR', 'ADVB']
    interesting_speech_parts = ['NOUN', 'NUMR', 'ADJF', 'ADJS', 'VERB']
    interesting_words_from_news = []
    for speech_parts in interesting_speech_parts:
        for word in words_from_news:
            parsed_word = morph.parse(word)[0]
            #print(parsed_word.tag)
            if speech_parts in parsed_word.tag:
                interesting_words_from_news.append(parsed_word.normal_form)

    interesting_words_from_title = []
    for speech_parts in interesting_speech_parts:
        for word in words_from_title:
            parsed_word = morph.parse(word)[0]
            if speech_parts in parsed_word.tag:
                interesting_words_from_title.append(parsed_word.normal_form)

    #print(interesting_words_from_title)
    all_intersting_words = interesting_words_from_news + interesting_words_from_title
    counted_words = Counter(all_intersting_words)

    for word in interesting_words_from_title:
        if word in counted_words:
            counted_words[word] *= 3

    key_words = []
    for word in counted_words:
        if counted_words[word] > 1:
            key_words.append(word)

    return(key_words)
