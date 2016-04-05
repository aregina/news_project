import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import pickle


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
    train = tf.fit_transform(text_train)
    # tags
    y = text.ix[:, 'tag']
    y = y.fillna('No tag')

    lr = LogisticRegression(penalty='l2', C=100)
    lr.fit(train, y)
    save_lr = pickle.dumps(lr)  # save trained algo
    return save_lr

teach()

def get_tags(news):
    tf = TfidfVectorizer(ngram_range=(1, 1))
    news_vectorized = tf.transform(news)
    lr_res = pickle.loads(teach().save_lr)

    res_proba = lr_res.predict_proba(news_vectorized)
    top_3_tags = []

    for probas in res_proba:
        cat_and_prob = [pair for pair in zip(probas, lr_res.classes_)]
        cat_and_prob.sort()
        top_3_tags.append([cat[1] for cat in cat_and_prob[-1:-4:-1] if cat[0] > 0.07])

    return top_3_tags
