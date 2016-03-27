import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.feature_extraction.text import TfidfVectorizer
import re

# Укажу число размеченных новостей и число новостей для маркировки
marked = 505
for_mark = 30
name_of_column = 'text' # имя колонки с новостью

# Читаю размеченную часть csv
Text = pd.read_csv('d.csv').ix[:marked+for_mark,0:6]

#приведу все новости к нижнему регистру
Text[name_of_column] = Text[name_of_column].apply(lambda x: re.sub('[^а-яА-Я]', ' ', x.lower()))

# превращаю новость числовой вектор и обучаюсь на нём.
Text_train = Text.ix[:marked,name_of_column]

tf = TfidfVectorizer(ngram_range = (1, 1))
X = tf.fit_transform(Text_train)

# колонка с категориями
y = Text.ix[:marked,'tag']
y = y.fillna('No tag')

# обучу логистическую регрессию

LR = LogisticRegression(penalty='l2', C=100)
LR.fit(X, y)


# прочитаю их файла ещё несколько новостей и попробую поставить на них тэги

X_test_raw = Text.ix[marked+1:marked+for_mark,name_of_column]
X_test = tf.transform(X_test_raw)

#################################### Выбор просто топового тэга ##############################
tags = LR.predict(X_test)

# Создаю индексы и полученный прогноз тегов объёдиняю в один датафрейм
index = [i for i in range(marked+1,marked+for_mark+1)]
tags = pd.DataFrame(tags, index=index)

# Соединяю тэги и тексты новостей
result_look = pd.concat([X_test_raw, tags], axis=1)

result_look.to_csv('res_look.csv')

#################################### Выбор 3-х топовых тэгов ##############################
# Выведу по 3 топовых тэга для каждой новости в отдельный датафрейм
# затем соединю в один фрейм сами новости и тэги для них
res_proba = LR.predict_proba(X_test)
top_3_tags = []

for probas in res_proba:
    cat_and_prob = [pair for pair in zip(probas, LR.classes_)]
    cat_and_prob.sort()
    top_3_tags.append([cat[1] for cat in cat_and_prob[-1:-4:-1] if cat[0] > 0.06]) #чтобы отсечь совсем маловероятные
    
index = [i for i in range(marked+1,marked+for_mark+1)]
tagged_news = pd.DataFrame(top_3_tags, index=index)

# Соединяю тэги и тексты новостей
result_look_3_tags = pd.concat([X_test_raw, tagged_news], axis=1)

result_look_3_tags.to_csv('res_look_3_tags.csv')
