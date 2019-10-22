import logging
from bs4 import BeautifulSoup

from . import q
from .visited import visited
from .requester import requester
from .link_processor import LinkProcessor


logger_main = logging.getLogger('main')

class PageProcessor:

    @staticmethod
    def run(url):
        with visited:
            if visited.was_processed(url):
                return
            else:
                visited.mark_processing(url)

        res = requester.get(url)

        if res.ok:
            PageProcessor.page_links(res.text, url)
        else:
            logger_main.error(res.raw)

        with visited:
            visited.mark_processed(url)

    @staticmethod
    def page_links(html, source_url):
        soup = BeautifulSoup(html, 'html.parser')
        tags = soup.find_all('a')

        for tag in tags:
            lp = LinkProcessor(tag, source_url)

            if lp.is_valid:
                q.put(lp.link)
