from utils import DjangoSetup  # setup django environment
from db.models import News, NewsText, UrlInText
from prjparser import textParser, urlOpen, aParser
from django import db
from django.db.models import QuerySet
from django.db import transaction


def parse_news_task_manager():
    for item in News.objects.filter(is_parsed=False)[:].iterator():
        yield item


def parse_news_worker(news: News):
    print(str(news.id) + "     ", end='\n')
    html = urlOpen.get_html(news.url)
    if html:
        text = textParser.get_text_from_html(html)
        return NewsText(news=news, text=text)


def parse_news_writer(news_text: NewsText):
    news_text.save()
    news_text.news.is_parsed = True
    news_text.news.save()


from multiprocessing import Process, Queue


def worker_function(worker, task_queue, result_queue):
    db.connection.close()
    while True:
        task = task_queue.get(timeout=10)
        if task == "end":
            break
        result = worker(task)
        #         task_queue.task_done()
        if result:
            result_queue.put(result)
    print("exit")


def invoke_worker_process(process_number, worker, task_queue, result_queue):
    process_list = []
    for i in range(process_number):
        p = Process(target=worker_function, args=(worker, task_queue, result_queue))
        p.start()
        process_list.append(p)
    return process_list


def task_process(task_function, task_queue):
    for task in task_function():
        task_queue.put(task)


def generate_end_signal(process_number, task_queue):
    for i in range(process_number):
        task_queue.put("end")


def check_process(process_list):
    status = []
    for p in process_list:
        status.append(p.is_alive())
    return any(status)


@transaction.atomic
def writer(write_function, result_queue, process_list):
    while not result_queue.empty() or check_process(process_list):
        try:
            result = result_queue.get(timeout=1)
        except:
            continue
        write_function(result)


def main():
    process_number = 20
    task_queue = Queue()
    result_queue = Queue()
    process_list = invoke_worker_process(process_number, parse_news_worker, task_queue, result_queue)
    task_process(parse_news_task_manager, task_queue)
    generate_end_signal(process_number, task_queue)
    writer(parse_news_writer, result_queue, process_list)


if __name__ == "__main__":
    main()
