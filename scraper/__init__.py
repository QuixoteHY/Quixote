# -*- coding:utf-8 -*-
# @Time     : 2019-02-20 23:09
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe : 引擎

import logging
from collections import deque

from quixote.protocol import Request, Response
from quixote.item import BaseItem
from quixote.utils.misc import load_object

logger = logging.getLogger(__name__)


class Slot(object):
    MIN_RESPONSE_SIZE = 1024

    def __init__(self, max_active_size=5000000):
        self.max_active_size = max_active_size
        self.queue = deque()
        self.active = set()
        self.active_size = 0
        self.itemproc_size = 0
        self.closing = None

    def add_response_request(self, response, request):
        self.queue.append((response, request))
        if isinstance(response, Response):
            self.active_size += max(len(response.body), self.MIN_RESPONSE_SIZE)
        else:
            self.active_size += self.MIN_RESPONSE_SIZE

    def next_response_request(self):
        response, request = self.queue.popleft()
        self.active.add(request)
        return response, request

    def finish_response(self, response, request):
        self.active.remove(request)
        if isinstance(response, Response):
            self.active_size -= max(len(response.body), self.MIN_RESPONSE_SIZE)
        else:
            self.active_size -= self.MIN_RESPONSE_SIZE

    def is_idle(self):
        return not (self.queue or self.active)

    def needs_slowdown(self):
        return self.active_size > self.max_active_size


class Scraper(object):
    def __init__(self, starter):
        self.slot = None
        # self.spidermw = SpiderMiddlewareManager.from_crawler(starter)
        itemmw_cls = load_object(starter.settings['ITEM_PROCESSOR'])
        self.itemmw = itemmw_cls.from_starter(starter)
        self.concurrent_items = starter.settings['CONCURRENT_ITEMS']
        self.starter = starter

    def open_spider(self, spider):
        """Open the given spider for scraping and allocate resources for it"""
        self.slot = Slot()
        self.itemmw.open_spider(spider)

    def enqueue_scrape2(self, response, request, spider):
        slot = self.slot
        try:
            slot.add_response_request(response, request)
            self._scrape_next(spider, slot)
            slot.finish_response(response, request)
            self._check_if_closing(spider, slot)
            self._scrape_next(spider, slot)
        except Exception as e:
            logger.error('Scraper bug processing %(request)s %(err)s', {'request': request, 'err': logger.exception(e)},
                         extra={'spider': spider})  # ,exc_info=failure_to_exc_info(f),

    def _scrape_next(self, spider, slot):
        while slot.queue:
            response, request = slot.next_response_request()
            self._scrape(response, request, spider)

    def _scrape(self, response, request, spider):
        """Handle the downloaded response or failure through the spider call_back/errback"""
        # assert isinstance(response, (Response, Failure))
        assert isinstance(response, Response)
        for result in self.call_parser(response, request, spider):
            self.handle_parser_output(result, request, response, spider)
        # self.handle_spider_error(result, request, response, spider)

    @staticmethod
    def call_parser(response, request, spider):
        response.request = request
        callback = request.callback or spider.parse
        for item_or_request in callback(response):
            yield item_or_request

    def handle_parser_output(self, result, request, response, spider):
        if isinstance(result, Request):
            self.starter.engine.crawl(request=result, spider=spider)
        elif isinstance(result, (BaseItem, dict)):
            self.slot.itemproc_size += 1
            output = self.itemmw.process_item(result, spider)
            self._itemproc_finished(output, result, response, spider)
            # print('Parsed\tstatus={}'.format(str(result['status'])+'\turl='+result['url']))
        elif result is None:
            pass
        else:
            logger.error('Spider must return Request, BaseItem, dict or None, got %(typename)r in %(request)s',
                         {'request': request, 'typename': type(result).__name__}, extra={'spider': spider})

    def _itemproc_finished(self, output, item, response, spider):
        self.slot.itemproc_size -= 1
        if output:
            print('Parsed\tstatus={}'.format(str(item['status']) + '\turl=' + item['url']
                                             + '\tpipeline=' + str(item['pipeline'])))
        else:
            print('Parsed Error...')

    def handle_spider_error(self, _failure, request, response, spider):
        pass

    def _check_if_closing(self, spider, slot):
        # if slot.closing and slot.is_idle():
        #     slot.closing.callback(spider)
        pass

    def enqueue_scrape(self, response, request, spider):
        for item_or_request in request.callback(response):
            print('Parsed {}'.format(item_or_request.decode()))
