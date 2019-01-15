
from quixote.downloader import Downloader

from quixote.test.test_spider import TestSpider
from quixote.protocol.request import Request
from quixote.starter import Starter

import asyncio


def parse():
    print('parse')


starter = Starter('quixote.test.test_spider.TestSpider')

r = Request(url='http://www.baidu.com', callback=parse)

spider = TestSpider()

d = Downloader(starter)

loop = asyncio.get_event_loop()

loop.run_until_complete(d.fetch(r, spider))
