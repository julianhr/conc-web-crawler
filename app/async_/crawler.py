import time
import logging
import asyncio as aio
from pyppeteer import launch

from . import q
from .visited import visited
from .metadata import metadata
from .requester import requester
from .link_processor import LinkProcessor


MAX_Q_IDLE_SEC = 60
NAP = 0.5
log_main = logging.getLogger('main')
log_enqueued_urls = logging.getLogger('enqueued_urls')

class Crawler:

    def __init__(self, init_url, run_for_sec=None):
        self.init_url = init_url
        self.run_for_sec = run_for_sec
        self.is_working = True
        self.start_ts = None

    def run(self):
        metadata.process_init_url(self.init_url)
        aio.run(self.main())

    async def setup(self):
        await requester.start()

    async def main(self):
        await self.setup()
        last_q_report_ts = time.time()

        try:
            browser = await launch()
            log_main.info(f'Crawler started, initial URL: {self.init_url}')
            self.start_ts = time.time()
            await q.put(self.init_url)

            while not q.empty() and self.is_working:
                url = q.get_nowait()
                await self.process(url, browser)
                ts = time.time()
                self.is_working = ts - self.start_ts < self.run_for_sec
        except Exception as err:
            log_main.exception(err)
        finally:
            await browser.close()
            await requester.close()

    async def process(self, url, browser):
        if visited.was_processed(url):
            return

        visited.mark_processing(url)
        log_main.info(f"processing {url}")

        try:
            res = await requester.head(url)

            if res.status >= 400:
                return

            page = await browser.newPage()
            await page.goto(url)
            links = await page.querySelectorAll('a')
            await self.process_links(links, url)
            visited.mark_processed(url)
        except Exception as err:
            log_main.exception(err)
        finally:
            await page.close()

    async def process_links(self, links, source_url):
        for link in links:
            prop = await link.getProperty('href')
            href = await prop.jsonValue()
            lp = LinkProcessor(href, source_url)
            await lp.run()

            if lp.is_valid:
                await q.put(lp.link)
                log_enqueued_urls = logging.getLogger('enqueued_urls')
