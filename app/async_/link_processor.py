import asyncio as aio
import logging
from urllib.parse import urlparse

from .requester import requester
from .metadata import metadata
from .host_verifier import HostVerifier


log_main = logging.getLogger('main')
log_rejected_urls = logging.getLogger('rejected_urls')

class LinkProcessor:

    INVALID_HREFS = { '', '#', '/' }

    def __init__(self, href, source_url):
        loop = aio.get_running_loop()
        self.href = href
        self.source_url = source_url
        self.parse_result = None
        self.link = None
        self.is_valid = True

    async def run(self):
        self.parse_result = pr = urlparse(self.href)

        try:
            if not await HostVerifier.is_valid(pr):
                raise ValueError(f"invalid host {self.parse_result.netloc} {self.href}")
            self.set_url_base(pr)
            self.verify_port(pr)
            self.set_path(pr)
        except ValueError as err:
            if self.href:
                log_rejected_urls.info(self.href)

            self.is_valid = False
        else:
            return True

    def set_url_base(self, pr):
        href = self.href

        if pr.scheme:
            if not (pr.scheme or '').startswith('http'):
                raise ValueError(f"invalid scheme {href}")

            if pr.netloc:
                self.link = f"{pr.scheme}://{pr.netloc}"
            else:
                raise ValueError(f"missing netloc {href}")
        else:
            if pr.netloc:
                raise ValueError(f"missing scheme {href}")
            else:
                self.link = self.source_url

        return True

    def verify_port(self, pr):
        if pr.port not in { None, 80, 443 }:
            raise ValueError(f"invalid port {pr.port} {self.href}")

    def set_path(self, pr):
        if pr.path:
            self.link += pr.path[:-1] if pr.path[-1] == '/' else pr.path
        else:
            if not pr.netloc:
                raise ValueError(f"URL is query, params or fragment {self.href}")
