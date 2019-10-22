import threading
from urllib.parse import urlparse


class Metadata:

    def __init__(self):
        self.url = None
        self.host = None
        self.domain = None
        self.parse_result = None

    def process_init_url(self, url):
        pr = urlparse(url)
        self.url = url
        self.host = pr.hostname
        self.domain = '.'.join(self.host.split('.')[-2:])
        self.parse_result = pr


metadata = Metadata()
