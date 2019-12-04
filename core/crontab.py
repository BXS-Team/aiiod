import threading
import _thread
import time
import signal
import os


def interuppt_handler(signum, frame):
    os._exit(0)


signal.signal(signal.SIGINT, interuppt_handler)
signal.signal(signal.SIGTERM, interuppt_handler)


class Task(object):
    def __init__(self, fn, args=None):
        self._fn = fn
        self._args = args

    def run(self):
        if self._args is not None:
            self._fn(*self._args)
        else:
            self._fn()


class Crontab(object):
    def __init__(self, tasks, duration=60):
        self._duration = duration
        self._tasks = tasks
        self._thread = threading.Thread(target=self._start)

    def _start(self):
        while True:
            try:
                for task in self._tasks:
                    threading.Thread(target=task.run).start()
            except Exception as e:
                print(e.__str__())
                continue
            time.sleep(self._duration)

    def start(self):
        _thread.start_new_thread(self._start, ())
        while True:
            input('Ctrl+C to exit\n')