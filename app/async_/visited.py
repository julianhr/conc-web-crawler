import collections
import logging


logger_visited_urls = logging.getLogger('visited_urls')

class Visited:

    def __init__(self):
        self.adj = collections.defaultdict(set)
        self.rejected_hosts = set()
        self.accepted_hosts = set()
        self.urls = {}

    def was_processed(self, url):
        return url in visited.urls

    def mark_processing(self, url):
        self.urls[url] = 'processing'

    def mark_processed(self, url):
        logger_visited_urls.info(url)
        self.urls[url] = 'processed'


visited = Visited()
