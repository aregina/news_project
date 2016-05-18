from django.shortcuts import render, get_object_or_404
from db.models import *
from django.db.models import Count, Max, Min, F, DecimalField, ExpressionWrapper
from django.http import JsonResponse, HttpResponse

MAX_RETURN = 5
MIN_RETURN = 1


# Create your views here.
def trivial_abs(value, max_v, min_v):
    return (value - min_v - 0.0) / (max_v - min_v) * (MAX_RETURN - MIN_RETURN) + MIN_RETURN


def get_news_list(key: KeyWord):
    return [{"name": news.title[:10]} for news in key.news.iterator()]


def test_index(request):
    return render(request, "db/index2.html", {})


def index(request):
    if 'json' in request.GET:
        news = News.objects.get(pk=1)
        res_dict = dict()
        res_dict["name"] = news.title[:20]
        res_dict["children"] = []
        for key in news.keyword_set.iterator():
            child = {"name": key.word, "children": get_news_list(key)}
            res_dict["children"].append(child)
        response = JsonResponse(res_dict)
        return response
    if 'json1' in request.GET:
        from django.db.models import Count
        news = News.objects \
            .extra({'y': 'strftime("%Y-%m-%d-%H",pub_date)'}) \
            .values('y') \
            .annotate(cnt=Count('pub_date'))
        return JsonResponse([n for n in news if "2016-04-24-02" < n['y'] < "2016-05-01-02"], safe=False)
    if 'json2' in request.GET:
        from django.db.models import Count
        from datetime import date
        news = News.objects \
            .extra({'y': 'strftime("%Y-%m-%d",pub_date)'}) \
            .values('y') \
            .annotate(cnt=Count('pub_date')) \
            .annotate(i=Min('id'))

        resp_dict = list()
        for n in news:
            first_day_news = News.objects.get(id=n['i'])
            n["n"] = first_day_news.title
            resp_dict.append(n)

        return JsonResponse(resp_dict, safe=False)
    # context = {"key": KeyWord.objects.get(word="путин")}
    context = {}
    return render(request, 'db/d3_2.html', context)


def tags(request, daily=False):
    key_query = KeyWord.objects
    if daily:
        key_query = key_query.filter(news__pub_date__day=3)
    key_query = key_query.annotate(cnt=Count('news')).filter(cnt__gt=20)
    key_range = key_query.aggregate(max=Max('cnt'), min=Min('cnt'))
    context = {"key": key_query.annotate(cnt_n=ExpressionWrapper(
        trivial_abs(F('cnt'), key_range['max'], key_range['min']), output_field=DecimalField(decimal_places=1)))}
    return render(request, 'db/tags.html', context)


# TODO переделать на один шаблон
def tag_detail(request, key_list=''):
    key_list = key_list.split('+')
    if len(key_list) == 1:
        key_word = get_object_or_404(KeyWord, word=key_list[0])
        context = {"key": key_word}
        return render(request, 'db/index.html', context)
    else:
        news = News.objects
        for key in key_list:
            if not key: continue
            news = news.filter(keyword__word=key)
        context = {"news_list": news, "key_list": key_list}
    return render(request, 'db/key_list.html', context)


def news_detail(request, news_id=0):
    news = get_object_or_404(News, pk=news_id)
    context = {"news": news}
    return render(request, 'db/news.html', context)
