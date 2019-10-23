import time
import logging
import asyncio as aio
from pyppeteer import launch

from . import q
from .metadata import metadata
from .requester import requester
from .scraper import Scraper


MAX_Q_IDLE_SEC = 60
NAP = 0.5
log_main = logging.getLogger('main')

class Crawler:

    def __init__(self, init_url, run_for_sec=None):
        self.init_url = init_url
        self.run_for_sec = run_for_sec

    def run(self):
        metadata.process_init_url(self.init_url)
        aio.run(self.main())

    async def main(self):
        await self.init()
        await q.put(self.init_url)
        log_main.info(f"Crawler started, initial URL: {self.init_url}")

        try:
            scrapers = [ aio.create_task(self.consumer(i+1)) for i in range(3) ]
            await aio.gather(*scrapers)
        except Exception as err:
            log_main.exception(err)

        await self.close()

    async def consumer(self, id):
        scraper = Scraper(id, self.run_for_sec)
        await scraper.run()

    async def init(self):
        await requester.start()

    async def close(self):
        await requester.close()
