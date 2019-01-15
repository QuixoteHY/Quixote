
from quixote.downloader.download_handlers import DownloadHandlers

from quixote.test.test_spider import TestSpider
from quixote.protocol.request import Request
from quixote.starter import Starter


def parse():
    print('parse')


s = Starter('quixote.test.test_spider.TestSpider')

r = Request(url='http://www.baidu.com', callback=parse)

spider = TestSpider()

dh = DownloadHandlers(s)

task = dh.download_request(r, spider)

print(task)

print(type(task))
