import time
import logging
import requests
from types import SimpleNamespace


logger_main = logging.getLogger('main')

class Requester:

    TIMEOUT = 20
    BACKOFFS = [5, 15, 30]
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
    }

    def __init__(self, timeout):
        self.session = requests.Session()
        self.req_verb = {
            'get': getattr(self.session, 'get'),
            'head': getattr(self.session, 'head'),
        }

    def _request(self, url, verb):
        res = SimpleNamespace(ok=False)

        for backoff in self.BACKOFFS:
            req = self.req_verb[verb]

            try:
                res = req(url, timeout=self.TIMEOUT, params=self.HEADERS)

                if res.ok:
                    return res
                else:
                    logger_main.warn(res.raw)
            except Exception as err:
                logger_main.error(err)
                time.sleep(backoff)

        return res

    def get(self, url):
        return self._request(url, 'get')

    def head(self, url):
        return self._request(url, 'head')


requester = Requester(20)
