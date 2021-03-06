from queue import Empty
from django.db import transaction
from django import db
from multiprocessing import Process, Queue


class MultiProc(object):
    end_signal = "end"
    num_of_write_queue = 300

    def __init__(self, process_number=10):
        self.task_queue = Queue()
        self.result_queue = Queue()
        self.process_number = process_number
# TODO использовать cpu_count

    def __call__(self):
        self.run()

    @staticmethod
    def worker(parse_obj):
        raise NotImplementedError

    @staticmethod
    def task_manager():
        raise NotImplementedError

    @staticmethod
    def writer(write_obj):
        raise NotImplementedError

    def __invoke_worker_process(self, worker_function):
        process_list = []
        for _ in range(self.process_number):
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
        for _ in range(self.process_number):
            self.task_queue.put(self.end_signal)

    def __is_any_alive_process(self):
        return any(p.is_alive() for p in self.process_list)

    def __writer(self, write_function):
        # TODO in MAC OS NotImplemented queue.qsize()
        import platform
        is_mac_os = True if platform.system() == "Darwin" else False
        while not self.result_queue.empty() or self.__is_any_alive_process():
            with transaction.atomic():
                # print("task queue {}".format(self.result_queue.qsize()))
                if not is_mac_os:
                    num = min(self.num_of_write_queue, self.result_queue.qsize())
                else:
                    num = 10
                # num = self.num_of_write_queue
                for i in range(num):
                    try:
                        result = self.result_queue.get(timeout=0.1)
                    except Empty:
                        continue
                    # TODO этот процесс должен всегда работать.
                    try:
                        write_function(result)
                    except Exception as e:
                        print(e)

    def run(self):
        self.__invoke_worker_process(self.worker)
        self.__invoke_task_process(self.task_manager)
        self.__writer(write_function=self.writer)
