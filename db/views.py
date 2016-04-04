from django.shortcuts import render,get_object_or_404
from db.models import *
from django.db.models import Count , Max, Min, F, DecimalField,ExpressionWrapper

MAX_RETURN = 5
MIN_RETURN = 1


# Create your views here.
def trivial_abs(value, max_v, min_v):
    return (value - min_v - 0.0) / (max_v - min_v) * (MAX_RETURN - MIN_RETURN) + MIN_RETURN


def index(request):
    context = {"key": KeyWord.objects.get(word="путин")}
    return render(request, 'db/index.html', context)


def tags(request):
    key_query = KeyWord.objects.annotate(cnt=Count('news')).filter(cnt__gt=20)
    key_range = key_query.aggregate(max=Max('cnt'), min=Min('cnt'))
    context = {"key": key_query.annotate(cnt_n=ExpressionWrapper(
        trivial_abs(F('cnt'), key_range['max'], key_range['min']), output_field=DecimalField(decimal_places=1)))}
    return render(request, 'db/tags.html', context)


def tag_detail(request, tag=''):
    key_word = get_object_or_404(KeyWord, word=tag)
    context = {"key": key_word}
    return render(request, 'db/index.html', context)
    #


def news_detail(request, news_id=0):
    news = get_object_or_404(News, pk=news_id)
    context = {"news": news}
    return render(request, 'db/news.html', context)
