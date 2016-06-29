import itertools

from django.core.paginator import Paginator
from django.db.models import Count, Max, Min, F, DecimalField, ExpressionWrapper
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from db.models import *

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


def news_per_day(request):
    news = News.objects
    if "related_news" in request.GET:
        news = news.get(pk=request.GET["related_news"]).related_news
    if "day" in request.GET:
        news = news.filter(pub_date__day=request.GET["day"])
    if "month" in request.GET:
        news = news.filter(pub_date__month=request.GET["month"])
    context = {"news_list": news, "key_list": [1,2]}
    return render(request, 'db/key_list.html', context)


def main_page(request):
    all_news = News.objects.all()
    paginator = Paginator(all_news, 6)
    page = request.GET.get('page', 1)
    news_list = paginator.page(page)
    # news = []
    # for i in range(7,13):
    #     news.append(News.objects.get(pk=i))
    context = {"news": news_list, "paginator": paginator}
    return render(request, 'db/main_page.html', context)


def news3_detail(request, news_id=0):
    news = get_object_or_404(News, pk=news_id)
    if news.newstext.is_emo_defined:
        emo = news.newstext.newsemotions.emo_weight
    else:
        emo = 0
    context = {"news": news, "emo": emo}
    return render(request, 'db/news3.html', context)


def related_news_json(request, news_id=0):
    main_news = get_object_or_404(News, pk=news_id)
    related_news = {"name": main_news.title, "children": []}
    for news in main_news.related_news:
        related_news_info = {"name": news.title, "size": 6714}
        related_news["children"].append(related_news_info)
    # main_news = get_object_or_404(News, pk=news_id)
    # related_news = {
    #      "name": main_news.title,
    #       "children": [
    #            {"name": "AgglomerativeCluster", "size": 10000},
    #            {"name": "CommunityStructure", "size": 10000},
    #            {"name": "HierarchicalCluster", "size": 10000},
    #            {"name": "MergeEdge", "size": 10000}
    #             ]
    #         }
    return JsonResponse(related_news)


def news_theme(request):
    all_news = News.objects.all()
    paginator = Paginator(all_news, 6)
    page = request.GET.get('page', 1)
    news_list = paginator.page(page)

    news_count = News.objects.count()
    all_news = News.objects.order_by('pub_date').all()
    sites_info = []
    all_sites = Site.objects.all()
    for current_site in all_sites:
        current_site_info = []
        current_site_info.append(current_site.name)
        news_per_site = all_news.filter(site__name=current_site.name).count()
        current_site_info.append(news_per_site*100//news_count)
        sites_info.append(current_site_info)

    emotions = [['Позитивные'], ['Негативные']]
    good_news_pers = (all_news.filter(newstext__newsemotions__emo_weight__gte=0.5).count()/news_count)*100
    emotions[0].append(good_news_pers)
    emotions[1].append(100 - good_news_pers)

    first_char_in_dates = ['x']
    dates = []
    news_count_per_day_1 = ['Количество новостей за последние дни']
    news_count_per_day = []
    for key, group in itertools.groupby(all_news, key=lambda x: str(x.pub_date.date())):
        dates.append(str(key))
        news_count_per_day.append(len(list(group)))

    full_dates = first_char_in_dates + dates[-6:]
    news_count_per_day_full = news_count_per_day_1 + news_count_per_day[-6:]

    context = { 'news': news_list,
                'news_count': news_count,
                'news_dates': full_dates,
                'news_count_per_day': news_count_per_day_full,
                'sites_info': sites_info,
                'emotions': emotions,
                }
    # print(report)
    return render(request, 'db/news_theme.html', context)
