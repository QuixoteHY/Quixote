
from quixote.downloader.download_handlers import DownloadHandlers

from quixote.test.test_spider.test_spider_cookies import DongmengSpider
from quixote.protocol.request import Request
from quixote.starter import Starter


def parse():
    print('parse')


s = Starter('quixote.test.test_spider.TestSpider')

r = Request(url='http://www.baidu.com', callback=parse)

spider = DongmengSpider()

dh = DownloadHandlers(s)

task = dh.download_request(r, spider)

print(task)

print(type(task))
