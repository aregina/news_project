import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news_project.settings")
django.setup()

from db.models import NewsTags, News
from prjparser import news_tags


def tags_create():
    # переменная news уже не news а news_text или что то вроде того и NewsText надо импортировать
    for news in NewsText.objects.filter(check_tag=False).iterator():
                                    # у news_text.news_text нет text =)
        tags_list = news_tags.get_tags(news.newstext.text)
        for tag in tags_list:
            try:
                # надо импортировать модель AllTags и AllTags.objects.get вернет не id а ссылку на обект
                tag_id = AllTags.objects.get(tag=tag[1])
                NewsTags.objects.create(news=news, weight=tag[0], tag=tag_id) # эту сточку можно вынести за
                                                                            # блок try и тогда не будет повтора
            except AllTags.DoesNotExist:  # <- лучше всегда уточнать какую ошибку ты перехватываешь
                tag_id = AllTags.objects.create(tag=tag[1])
                NewsTags.objects.create(news=news, weight=tag[0], tag=tag_id)
                
        news.check_tag = True
        news.save()


if __name__ == "__main__":
    tags_create()
