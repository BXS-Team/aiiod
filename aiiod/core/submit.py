import queue
import time
import threading
import _thread

from aiiod.core.utils import singleton
import aiiod.core.logger as logger


@singleton
class Submiter(object):
    RETRY = 3
    RETRY_DURATION = 3

    def __init__(self, submit_flag_fn, delay=0):
        self._flag_lst = queue.Queue()
        self._exit = False
        self._thread = None
        self._submit_flag_fn = submit_flag_fn
        self._delay = delay
        # self._max_workers = max_workers

    def add_flag(self, flag: dict):
        """flag should be a dict such as `{'flag': '', 'ip': ''}`"""
        if not isinstance(flag, dict):
            flag = {'flag': flag}
        for k in flag.keys():
            flag[k] = flag[k].strip()
        self._flag_lst.put(flag)

    def submit_flags(self):
        while not self._exit:
            try:
                flag = self._flag_lst.get()
                self._submit_flag_fn(**flag)
                time.sleep(self._delay)
            except Exception as e:
                logger.error(e.__str__())

    def submit_flag_with_retry(self):
        while True:
            retry = self.RETRY + 2
            flag = ''

            try:
                flag = self._flag_lst.get_nowait()
            except queue.Empty:
                pass

            while retry and not flag:
                time.sleep(self.RETRY_DURATION)
                try:
                    flag = self._flag_lst.get_nowait()
                except queue.Empty:
                    pass
                retry -= 1

            if flag:
                success = self._submit_flag_fn(**flag)
                _retry = self.RETRY - 1

                while not success and _retry:
                    time.sleep(self.RETRY_DURATION)
                    _retry -= 1
                    success = self._submit_flag_fn(**flag)

            if not retry:
                break

    def _start(self):
        _thread.start_new_thread(self.submit_flags, ())
        while not self._exit:
            time.sleep(1)

    def start(self):
        if self._thread is not None and self._thread.is_alive():
            self._exit = True
            time.sleep(2)
            self._exit = False

        self._thread = threading.Thread(target=self._start)
        self._thread.start()

    def exit(self):
        self._exit = True

    """
    async def submit_flag(self):
        while True:
            retry = self.RETRY - 1
            flag = ''

            try:
                flag = self._flag_lst.get_nowait()
            except queue.Empty:
                pass

            while retry and not flag:
                await asyncio.sleep(self.RETRY_DURATION)
                try:
                    flag = self._flag_lst.get_nowait()
                except queue.Empty:
                    pass
                retry -= 1

            if flag:
                success = await self._submit_flag_fn(flag[0], flag[1])
                _retry = self.RETRY - 1

                while not success and _retry:
                    await asyncio.sleep(self.RETRY_DURATION)
                    _retry -= 1
                    success = await self._submit_flag_fn(flag[0], flag[1])

            if not retry:
                break

    def start(self):
        try:
            loop = asyncio.get_event_loop()
            tasks = [
                asyncio.ensure_future(self.submit_flag())
                for _ in range(self._max_workers)
            ]
            loop.run_until_complete(asyncio.gather(*tasks))

        finally:
            loop.close()
    """