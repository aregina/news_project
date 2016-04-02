import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
import re

# Укажу число размеченных новостей и число новостей для маркировки
marked = 505
for_mark = 30
name_of_column = 'text'  # имя колонки с новостью

# Читаю размеченную часть csv
Text = pd.read_csv('teacher.csv').ix[:marked + for_mark, 0:6]

# приведу все новости к нижнему регистру и избавлюсь от лишнего
Text[name_of_column] = Text[name_of_column].apply(lambda x: re.sub('[^а-яА-Я]', ' ', x.lower()))

# превращаю новость в числовой вектор и обучаюсь на нём.
Text_train = Text.ix[:marked, name_of_column]

tf = TfidfVectorizer(ngram_range=(1, 1))
X = tf.fit_transform(Text_train)

# колонка с категориями
y = Text.ix[:marked, 'tag']
y = y.fillna('No tag')

# обучу логистическую регрессию

LR = LogisticRegression(penalty='l2', C=100)
LR.fit(X, y)
