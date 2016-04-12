import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import pickle
from math import trunc


def teach():
    # Initial data
    marked = 505
    name_of_column = 'text'  # column with news
    text = pd.read_csv('teacher.csv').ix[:marked, 0:6]
    # clean text
    text[name_of_column] = text[name_of_column].apply(lambda x: re.sub('[^а-яА-Я]', ' ', x.lower()))

    # tf-idf
    text_train = text.ix[:, name_of_column]
    tf = TfidfVectorizer(ngram_range=(1, 1))
    algo = tf.fit(text_train)
    train = tf.transform(text_train)
    tf_file = open('tf.txt', 'br+')
    pickle.dump(algo, tf_file)
    tf_file.close()
    # tags
    y = text.ix[:, 'tag']
    y = y.fillna('No tag')
    lr = LogisticRegression(penalty='l2', C=100)
    lr.fit(train, y)

    lr_file = open('lr.txt', 'br+')
    pickle.dump(lr, lr_file)
    lr_file.close()

teach()


def get_tags(news):
    tf_file = open('tf.txt', 'br')
    tf_pickled = tf_file.read()
    tf = pickle.loads(tf_pickled)
    tf_file.close()

    news = [news]
    news_vectorized = tf.transform(news)

    # take lr algo from file
    lr_file = open('lr.txt', 'br')
    lr_pickled = lr_file.read()
    lr = pickle.loads(lr_pickled)
    lr_file.close()

    res_proba = lr.predict_proba(news_vectorized)
    top_3_tags = []

    cat_and_prob = [pair for pair in zip(res_proba[0], lr.classes_)]
    cat_and_prob.sort()
    top_3_tags.append([[trunc(cat[0]*100), cat[1]] for cat in cat_and_prob[-1:-4:-1] if cat[0] > 0.07])

    return top_3_tags

if __name__ == "__main__":
    get_tags()