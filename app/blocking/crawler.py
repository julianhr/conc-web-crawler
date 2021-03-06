import queue
import threading
import logging
from .scraper import Scraper
from .metadata import metadata
from . import q


logger_main = logging.getLogger('main')

class Crawler:

    def __init__(self, init_url, num_threads, run_for_sec=None):
        self.init_url = init_url
        self.num_threads = num_threads
        self.run_for_sec = run_for_sec
        self.threads = self.get_threads(num_threads)

    def get_threads(self, num_threads):
        threads = []

        for i in range(num_threads):
            scraper = Scraper(f'cons-{i+1}', self.run_for_sec)
            threads.append(scraper)

        return threads

    def run(self):
        metadata.process_init_url(self.init_url)
        q.put(self.init_url)
        logger_main.info(f'Crawler started, initial URL: {self.init_url}')

        for th in self.threads:
            th.start()

        for th in self.threads:
            th.join()
