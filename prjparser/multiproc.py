from queue import Empty

from django.db import transaction
from django import db
from multiprocessing import Process, Queue


class MultiProc:
    end_signal = "end"

    def __init__(self, process_number=10):
        self.task_queue = Queue()
        self.result_queue = Queue()
        self.process_number = process_number

    def worker(self, parse_obj):
        raise NotImplementedError

    def task_manager(self):
        raise NotImplementedError

    def writer(self, write_obj):
        raise NotImplementedError

    def __invoke_worker_process(self, worker_function):
        process_list = []
        for i in range(self.process_number):
            p = Process(target=self.__worker_process, args=(worker_function,))
            p.start()
            process_list.append(p)
        self.process_list = process_list

    def __worker_process(self, worker):
        db.connection.close()
        while True:
            task = self.task_queue.get(timeout=10)
            if task == self.end_signal:
                break
            result = worker(task)
            # task_queue.task_done()
            if result:
                self.result_queue.put(result)

    def __invoke_task_process(self, task_function):
        p = Process(target=self.__task_process, args=(task_function,))
        p.start()

    def __task_process(self, task_function):
        for task in task_function():
            self.task_queue.put(task)
        # generate end signal
        for i in range(self.process_number):
            self.task_queue.put(self.end_signal)

    def __check_process(self):
        status = []
        for p in self.process_list:
            status.append(p.is_alive())
        return any(status)

    @transaction.atomic
    def __writer(self, write_function):
        while not self.result_queue.empty() or self.__check_process():
            try:
                result = self.result_queue.get(timeout=0.1)
            except Empty:
                continue
            write_function(result)

    def run(self):
        self.__invoke_worker_process(self.worker)
        self.__invoke_task_process(self.task_manager)
        self.__writer(write_function=self.writer)
