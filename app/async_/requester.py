import asyncio as aio
import aiohttp
import logging
from types import SimpleNamespace


TIMEOUT = 20
BACKOFFS = [5, 15, 30]
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
}
logger_main = logging.getLogger('main')

class Requester:

    def __init__(self, timeout):
        self.session = None

    async def start(self):
        self.session = aiohttp.ClientSession()

    async def close(self):
        await self.session.close()

    async def _request(self, url, verb):
        res = SimpleNamespace(ok=False)

        for backoff in BACKOFFS:
            req = getattr(self.session, verb)

            try:
                async with req(url, params=HEADERS) as res:
                    if res.status < 400:
                        return res
                    else:
                        logger_main.warn(res.text())
            except Exception as err:
                logger_main.exception(err)
                await aio.sleep(backoff)

        return res

    async def get(self, url):
        return await self._request(url, 'get')

    async def head(self, url):
        return await self._request(url, 'head')


requester = Requester(20)
