# import pandas as pd
# from sklearn.linear_model import LogisticRegression
# from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
from math import trunc
from pymorphy2 import MorphAnalyzer as MA

# def teach():
#     # Initial data
#     marked = 1004
#     name_of_column = 'text'  # column with news
#     text = pd.read_csv('prjparser/teacher_new.csv').ix[:marked, 0:6]
#
#     text_train = text.ix[:, name_of_column]
#     morph = MA()
#     for i, news in enumerate(text_train):
#         normalized_news = " ".join([morph.parse(word)[0].normal_form for word in news.split()])
#         text.ix[i, name_of_column] = normalized_news
#         print(i)
#
#
#     tf = TfidfVectorizer(ngram_range=(1, 1))
#     tf.fit(text_train)
#     train = tf.transform(text_train)
#     with open('prjparser/tf.txt', 'br+') as tf_file:
#         pickle.dump(tf, tf_file)
#
#     y = text.ix[:, 'tag']
#     lr = LogisticRegression(penalty='l2', C=100)
#     lr.fit(train, y)
#
#     with open('prjparser/lr.txt', 'br+') as lr_file:
#         pickle.dump(lr, lr_file)
#
# teach()


def get_tags(news):
    # with open('prjparser/tf.txt', 'br') as tf_file:
    #     tf_pickled = tf_file.read()
    #     tf = pickle.loads(tf_pickled)

    # morph = MA()
    # normalized_news = [" ".join([morph.parse(word)[0].normal_form for word in news.split()])]
    news_vectorized = tf.transform([news])

    # with open('prjparser/lr.txt', 'br') as lr_file:
    #     lr_pickled = lr_file.read()
    #     lr = pickle.loads(lr_pickled)

    res_proba = lr.predict_proba(news_vectorized)
    top_3_tags = []

    cat_and_prob = [pair for pair in zip(res_proba[0], lr.classes_)]
    cat_and_prob.sort()
    top_3_tags.append([[trunc(cat[0]*100), cat[1]] for cat in cat_and_prob[-1:-4:-1] if cat[0] > 0.07])

    return top_3_tags

if __name__ == "__main__":
    pass
else:
    with open('prjparser/tf.txt', 'br') as tf_file:
        tf_pickled = tf_file.read()
        tf = pickle.loads(tf_pickled)

    with open('prjparser/lr.txt', 'br') as lr_file:
        lr_pickled = lr_file.read()
        lr = pickle.loads(lr_pickled)
