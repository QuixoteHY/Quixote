
from scrapy.statscollectors import MemoryStatsCollector
from quixote.test.test_spider.test_spider_cookies4 import TestCookiesSpider


spider = TestCookiesSpider()


msc = MemoryStatsCollector(True)

msc.inc_value('aaa', spider=spider)
msc.inc_value('bbb', spider=spider)
msc.inc_value('aaa', spider=spider)
msc.inc_value('ccc', spider=spider)
msc.inc_value('aaa', spider=spider)


msc.close_spider(spider, 'None')







