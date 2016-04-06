from utils import DjangoSetup

from multiprocessing import JoinableQueue, Process, Queue
from db.models import News
from prjparser import urlOpen, textParser
import os


def info():
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())


def worker(input_q: JoinableQueue, output: Queue):
    from django import db
    db.connection.close()
    while True:
        task = input_q.get()
        if task == "end":
            break
        html = urlOpen.get_html(task.url)
        if html:
            text = textParser.get_text_from_html(html)
        input_q.task_done()
        # info()
        output.put(task.url)
    print("exit")


def check_process(process_list):
    status = []
    for p in process_list:
        status.append(p.is_alive())
    return any(status)


def task_writer(task: JoinableQueue):
    for n in News.objects.all()[:50].iterator():
        task.put(n)

    for i in range(PROCESS_NUM):
        task.put("end")
    print("task writer ends")


task_queue = JoinableQueue()
result_queue = Queue()

PROCESS_NUM = 4
process_list = []

for i in range(PROCESS_NUM):
    p = Process(target=worker, args=(task_queue, result_queue))
    p.start()
    process_list.append(p)

task_w = Process(target=task_writer,args=(task_queue,))
task_w.start()


# task_queue.join()

print(result_queue.qsize())

while not result_queue.empty() or check_process(process_list):
    try:
        print(result_queue.get(timeout=2))
    except:
        print("await data")
