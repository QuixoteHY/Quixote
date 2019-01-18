
from quixote.downloader.download_handler.http_download_handler import HTTPDownloadHandler

from quixote.test.test_spider import TestSpider
from quixote.protocol.request import Request
from quixote.settings import Settings
from quixote.settings import settings

import asyncio

import functools


def parse():
    print('parse')


async def close(dd, future):
    dd.session.close()


r = Request(url='http://localhost:8000/reverse/11254', callback=parse)

spider = TestSpider()

d = HTTPDownloadHandler(Settings(settings).get_settings())


task = asyncio.ensure_future(d._download(r, spider))
task.add_done_callback(functools.partial(close, d))

loop = asyncio.get_event_loop()

loop.run_until_complete(task)

loop.close()
