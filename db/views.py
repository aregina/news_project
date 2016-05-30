from django.shortcuts import render, get_object_or_404
from db.models import *
from django.db.models import Count, Max, Min, F, DecimalField, ExpressionWrapper
from django.http import JsonResponse

MAX_RETURN = 5
MIN_RETURN = 1


def trivial_abs(value, max_v, min_v):
    return (value - min_v - 0.0) / (max_v - min_v) * (MAX_RETURN - MIN_RETURN) + MIN_RETURN


def index(request):
    if 'json1' in request.GET:
        from django.db.models import Count
        news = News.objects \
            .extra({'y': 'strftime("%Y-%m-%d-%H",pub_date)'}) \
            .values('y') \
            .annotate(cnt=Count('pub_date'))
        return JsonResponse([n for n in news if "2016-04-24-02" < n['y'] < "2016-05-01-02"], safe=False)
    if 'json2' in request.GET:
        from django.db.models import Count
        news = News.objects \
            .extra({'y': 'date(pub_date)'}) \
            .values('y') \
            .annotate(cnt=Count('pub_date')) \
            .annotate(i=Min('id'))

        resp_dict = list()
        for n in news:
            first_day_news = News.objects.get(id=n['i'])
            n["n"] = first_day_news.title
            resp_dict.append(n)

        return JsonResponse(resp_dict, safe=False)
    context = {}
    return render(request, 'db/index2.html', context)


def tags(request, daily=False):
    key_query = KeyWord.objects
    if daily:
        key_query = key_query.filter(news__pub_date__day=15, news__pub_date__month=4)
        key_query = key_query.annotate(cnt=Count('news'))
    else:
        key_query = key_query.annotate(cnt=Count('news')).filter(cnt__gt=1000)[:150]
    key_range = key_query.aggregate(max=Max('cnt'), min=Min('cnt'))
    context = {"key": key_query.annotate(cnt_n=ExpressionWrapper(
        trivial_abs(F('cnt'), key_range['max'], key_range['min']), output_field=DecimalField(decimal_places=1)))}
    return render(request, 'db/tags.html', context)


def tag_detail(request, key_list=''):
    key_list = key_list.split('+')
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


def new_news_detail(request, news_id=0):
    if 'json' in request.GET:
        news = News.objects.get(pk=news_id)
        return JsonResponse([{"id": n.pk, "date": n.pub_date} for n in news.related_news.iterator()], safe=False)

    news = get_object_or_404(News, pk=news_id)
    context = {"news": news}
    return render(request, 'db/news2.html', context)
