import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import pickle
from math import trunc


def teach_emo():
    # Initial data
    marked = 129
    name_of_column = 'text'  # column with news
    text = pd.read_csv('teacher_emo.csv').ix[:marked, 0:4]
    # clean text
    text[name_of_column] = text[name_of_column].apply(lambda x: re.sub('[^а-яА-Я]', ' ', x.lower()))

    # tf-idf
    text_train = text.ix[:, name_of_column]
    tf = TfidfVectorizer(ngram_range=(1, 1))
    algo = tf.fit(text_train)
    train = tf.transform(text_train)
    tf_file = open('tf_emo.txt', 'br+')
    pickle.dump(algo, tf_file)
    tf_file.close()
    # tags
    y = text.ix[:, 'emo']
    y = y.fillna('No tag')
    lr = LogisticRegression(penalty='l2', C=100)
    lr.fit(train, y)

    lr_file = open('lr_emo.txt', 'br+')
    pickle.dump(lr, lr_file)
    lr_file.close()

teach_emo()


def get_emotions(news):
    tf_file = open('tf_emo.txt', 'br')
    tf_pickled = tf_file.read()
    tf = pickle.loads(tf_pickled)
    tf_file.close()

    news = [news]
    news_vectorized = tf.transform(news)

    # take lr algo from file
    lr_file = open('lr_emo.txt', 'br')
    lr_pickled = lr_file.read()
    lr = pickle.loads(lr_pickled)
    lr_file.close()

    res_proba_of_emo = lr.predict_proba(news_vectorized)

    probability_of_good = res_proba_of_emo[0][1]

    print(lr.classes_)
    print(probability_of_good)

    return probability_of_good

if __name__ == "__main__":
    get_emotions("Любовь построили и победили")