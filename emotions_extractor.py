from utils import DjangoSetup
from db.models import NewsText, NewsEmotions
from prjparser import news_emotions
from django.db import transaction


@transaction.atomic
def emo_define():
    for news_text in NewsText.objects.filter(is_emo_defined=False).iterator():
        emo_weight = news_emotions.get_emotions(news_text.text)
        NewsEmotions.objects.create(news=news_text, emo_weight=emo_weight*100)
        news_text.is_emo_defined = True
        news_text.save()
        print(emo_weight*100)

if __name__ == "__main__":
    emo_define()
