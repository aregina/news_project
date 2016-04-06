from django.db import transaction
from django import db
from multiprocessing import Process, Queue


class MultiProc:
    def __init__(self, process_number=10):
        self.task_queue = Queue()
        self.result_queue = Queue()
        self.process_number = process_number

    def __worker_function(self, worker):
        db.connection.close()
        while True:
            task = self.task_queue.get(timeout=10)
            if task == "end":
                break
            result = worker(task)
            # task_queue.task_done()
            if result:
                self.result_queue.put(result)
        print("exit")

    def __invoke_worker_process(self, worker_function):
        process_list = []
        for i in range(self.process_number):
            p = Process(target=self.__worker_function, args=(worker_function,))
            p.start()
            process_list.append(p)
        self.process_list = process_list

    def __task_process(self, task_function):
        for task in task_function():
            self.task_queue.put(task)

    def __generate_end_signal(self):
        for i in range(self.process_number):
            self.task_queue.put("end")

    def __check_process(self):
        status = []
        for p in self.process_list:
            status.append(p.is_alive())
        return any(status)

    @transaction.atomic
    def __writer(self, write_function):
        while not self.result_queue.empty() or self.__check_process():
            try:
                result = self.result_queue.get(timeout=1)
            except:
                continue
            write_function(result)

    def run(self):
        self.__invoke_worker_process()
        task_process(parse_news_task_manager, task_queue)
        generate_end_signal(process_number, task_queue)
        writer(parse_news_writer, result_queue, process_list)
