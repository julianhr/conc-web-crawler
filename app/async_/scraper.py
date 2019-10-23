import time
import logging
from pyppeteer import launch

from . import q
from .visited import visited
from .requester import requester


log_main = logging.getLogger('main')
log_enqueued_urls = logging.getLogger('enqueued_urls')

class Scraper:

    def __init__(self, scraper_id, run_for_sec):
        self.id = f"[cons-{scraper_id}]"
        self.run_for_sec = run_for_sec
        self.is_working = True
        self.start_ts = None

    async def run(self):
        log_main.info(f"{self.id} Scraper started")
        last_q_report_ts = time.time()
        browser = await launch()
        self.start_ts = time.time()

        while self.is_working:
            try:
                while not q.empty() and self.is_working:
                    url = q.get_nowait()
                    await self.scrape(url, browser)
                    self.set_is_working()
            except aio.QueueEmpty:
                aio.sleep(0.5)
            except Exception as err:
                log_main.exception(err)

            self.set_is_working()

        await browser.close()

    async def scrape(self, url, browser):
        if visited.was_processed(url):
            return

        visited.mark_processing(url)
        log_main.info(f"{self.id} processing {url}")
        page = None

        try:
            res = await requester.head(url)

            if res.status >= 400:
                return

            page = await browser.newPage()
            await page.goto(url)
            links = await page.querySelectorAll('a')
            await self.crawl_links(links, url)
            visited.mark_processed(url)
        except Exception as err:
            log_main.exception(err)
        finally:
            if page:
                await page.close()

    async def crawl_links(self, links, source_url):
        for link in links:
            prop = await link.getProperty('href')
            href = await prop.jsonValue()
            lp = LinkProcessor(href, source_url)
            await lp.run()

            if lp.is_valid:
                await q.put(lp.link)
                log_enqueued_urls.info(lp.link, self.id)

    def set_is_working(self):
        if self.run_for_sec is not None:
            t1 = time.time()
            self.is_working = t1 - self.start_ts < self.run_for_sec
