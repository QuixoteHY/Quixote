
from quixote.state.statecollector import MemoryStatsCollector
from quixote.starter import Starter
from quixote.test.test_spider.test_spider_cookies3 import TestCookiesSpider


spider = TestCookiesSpider()


s = Starter('quixote.test.test_spider.test_spider_cookies3.TestCookiesSpider')
msc = MemoryStatsCollector(s)

msc.inc_value('aaa', spider=spider)
msc.inc_value('bbb', spider=spider)
msc.inc_value('aaa', spider=spider)
msc.inc_value('ccc', spider=spider, count=23)
msc.inc_value('aaa', spider=spider)


msc.close_spider(spider, 'None')


print(msc.spider_stats)







