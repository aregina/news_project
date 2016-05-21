import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
from pymorphy2 import MorphAnalyzer as MA


# def teach_emo():
#     # Initial data
#     marked = 299
#     name_of_column = 'text'  # column with news
#     text = pd.read_csv('prjparser/teacher_emo.csv').ix[:marked, 0:4]
#
#     text_train = text.ix[:, name_of_column]
#     morph = MA()
#     for i, news in enumerate(text_train):
#         normalized_news = " ".join([morph.parse(word)[0].normal_form for word in news.split()])
#         text.ix[i, name_of_column] = normalized_news
#         print(i)
#
#     tf = TfidfVectorizer(ngram_range=(1, 1))
#     tf.fit(text_train)
#     train = tf.transform(text_train)
#
#     with open('prjparser/tf_emo.txt', 'br+') as tf_file:
#         pickle.dump(tf, tf_file)
#
#     # tags
#     y = text.ix[:, 'emo']
#     lr = LogisticRegression(penalty='l2', C=100)
#     lr.fit(train, y)
#
#     with open('prjparser/lr_emo.txt', 'br+') as lr_file:
#         pickle.dump(lr, lr_file)
#
# teach_emo()

with open('prjparser/tf_emo.txt', 'br') as tf_file:
    tf_pickled = tf_file.read()
    tf = pickle.loads(tf_pickled)

with open('prjparser/lr_emo.txt', 'br') as lr_file:
    lr_pickled = lr_file.read()
    lr = pickle.loads(lr_pickled)

def get_emotions(news):
    # with open('prjparser/tf_emo.txt', 'br') as tf_file:
    #     tf_pickled = tf_file.read()
    #     tf = pickle.loads(tf_pickled)

    news_vectorized = tf.transform([news])

    # with open('prjparser/lr_emo.txt', 'br') as lr_file:
    #     lr_pickled = lr_file.read()
    #     lr = pickle.loads(lr_pickled)

    res_proba_of_emo = lr.predict_proba(news_vectorized)
    probability_of_good = res_proba_of_emo[0][1]

    return probability_of_good

if __name__ == "__main__":
    pass
else:
    with open('prjparser/tf.txt', 'br') as tf_file:
        tf_pickled = tf_file.read()
        tf = pickle.loads(tf_pickled)

    with open('prjparser/lr.txt', 'br') as lr_file:
        lr_pickled = lr_file.read()
        lr = pickle.loads(lr_pickled)
