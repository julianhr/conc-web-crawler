import threading
import time
import queue
import logging

from .page_processor import PageProcessor
from . import q


MAX_Q_IDLE_SEC = 60
NAP = 0.5
logger_main = logging.getLogger('main')

class Crawler(threading.Thread):

    def __init__(self, thread_name, run_for_sec):
        threading.Thread.__init__(self, name=thread_name)
        self.run_for_sec = run_for_sec
        self.is_working = True
        self.q_report_freq_sec = 5
        self.start_timestamp = None
        self.last_q_report_ts = None

    def run(self):
        self.start_timestamp = time.time()
        logger_main.info(f'thread {threading.current_thread().name} started')

        while self.is_working:
            self.execute_work()

            if self.is_working:
                time.sleep(NAP)

            self.set_is_working()

    def execute_work(self):
        self.last_q_report_ts = time.time()

        while not q.empty() and self.is_working:
            try:
                url = q.get(MAX_Q_IDLE_SEC)
                logger_main.info(f'process {url}')
                self.q_report()
                PageProcessor.run(url)
                q.task_done()
            except queue.Empty as err:
                logger_main.info(err)
                self.is_working = False

            self.set_is_working()

    def set_is_working(self):
        if self.run_for_sec is not None:
            t0 = self.start_timestamp
            t1 = time.time()
            self.is_working = t1 - t0 < self.run_for_sec


    def q_report(self):
        ts = time.time()

        if ts - self.last_q_report_ts > self.q_report_freq_sec:
            logger_main.info(f"Queue size: {q.qsize()}")
            self.last_q_report_ts = ts
