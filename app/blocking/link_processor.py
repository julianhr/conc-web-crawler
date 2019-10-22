import urllib.parse
import logging
from .host_verifier import HostVerifier
from .metadata import metadata


logger_rejected_urls = logging.getLogger('rejected_urls')
logger_enqueued_urls = logging.getLogger('enqueued_urls')

class LinkProcessor:

    INVALID_HREFS = { '', '#', '/' }

    def __init__(self, tag, source_url):
        self.tag = tag
        self.source_url = source_url
        self.parse_result = None
        self.link = None
        self.is_valid = self.process()

    def process(self):
        self.href = self.tag.get('href', '').lower().strip()
        self.parse_result = pr = urllib.parse.urlparse(self.href)

        try:
            if not HostVerifier.is_valid(pr):
                raise ValueError(f"invalid host {self.parse_result.netloc} {self.href}")
            self.set_url_base(pr)
            self.verify_port(pr)
            self.set_path(pr)
        except ValueError as err:
            if self.href:
                logger_rejected_urls.info(self.href)

            return False
        else:
            logger_enqueued_urls.info(self.href)
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
