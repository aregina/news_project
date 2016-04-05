import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import pickle

# Initial data 
marked = 505
for_mark = 30
name_of_column = 'text'  # column with news
Text = pd.read_csv('teacher.csv').ix[:marked + for_mark, 0:6]

# clean text
Text[name_of_column] = Text[name_of_column].apply(lambda x: re.sub('[^а-яА-Я]', ' ', x.lower()))

# tf-idf
Text_train = Text.ix[:marked, name_of_column]
tf = TfidfVectorizer(ngram_range=(1, 1))
X = tf.fit_transform(Text_train)

# tags
y = Text.ix[:marked, 'tag']
y = y.fillna('No tag')

LR = LogisticRegression(penalty='l2', C=100)
LR.fit(X, y)
save_LR = pickle.dumps(LR) # save trained algo


def get_tags(news):
	news_vectorized = tf.transform(news)
	LR_res = pickle.loads(save_LR)

	res_proba = LR_res.predict_proba(news_vectorized)
	top_3_tags = []

	for probas in res_proba:
		cat_and_prob = [pair for pair in zip(probas, LR_res.classes_)]
		cat_and_prob.sort()
		top_3_tags.append([cat[1] for cat in cat_and_prob[-1:-4:-1] if cat[0] > 0.07])

	return (top_3_tags)
