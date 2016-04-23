import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import pickle
from math import trunc
from pymorphy2 import MorphAnalyzer as MA


def teach_emo():
    # Initial data
    marked = 299
    name_of_column = 'text'  # column with news
    text = pd.read_csv('teacher_emo.csv').ix[:marked, 0:4]
    # clean text
    text[name_of_column] = text[name_of_column].apply(lambda x: re.sub('[^а-яА-Я]', ' ', x.lower()))

    text_train = text.ix[:, name_of_column]
    morph = MA()
    for i, news in enumerate(text_train):
        normalized_news = " ".join([morph.parse(word)[0].normal_form for word in news.split()])
        text.ix[i, name_of_column] = normalized_news
        print(i)

    tf = TfidfVectorizer(ngram_range=(1, 1))
    algo = tf.fit(text_train)
    train = tf.transform(text_train)

    with open('tf_emo.txt', 'br+') as tf_file:
        pickle.dump(algo, tf_file)

    # tags
    y = text.ix[:, 'emo']
    y = y.fillna('No tag')
    lr = LogisticRegression(penalty='l2', C=100)
    lr.fit(train, y)

    with open('lr_emo.txt', 'br+') as lr_file:
        pickle.dump(algo, lr_file)

teach_emo()


def get_emotions(news):
    with open('tf_emo.txt', 'br') as tf_file:
        tf_pickled = tf_file.read()
        tf = pickle.loads(tf_pickled)

    news = [news]
    news_vectorized = tf.transform(news)

    # take lr algo from file
    with open('lr_emo.txt', 'br') as lr_file:
        lr_pickled = lr_file.read()
        lr = pickle.loads(lr_pickled)

    res_proba_of_emo = lr.predict_proba(news_vectorized)

    probability_of_good = res_proba_of_emo[0][1]

    print(lr.classes_)
    print(probability_of_good)

    return probability_of_good

if __name__ == "__main__":
    get_emotions()