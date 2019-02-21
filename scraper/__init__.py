# -*- coding:utf-8 -*-
# @Time     : 2019-02-20 23:09
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe : 引擎

import logging
from collections import deque

from quixote.protocol import Response
from quixote.utils.misc import load_object

logger = logging.getLogger(__name__)


class Slot(object):
    MIN_RESPONSE_SIZE = 1024

    def __init__(self, max_active_size=5000000):
        self.max_active_size = max_active_size
        self.queue = deque()
        self.active = set()
        self.active_size = 0
        self.itemmw_size = 0
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

    def enqueue_scrape(self, response, request, spider):
        slot = self.slot
        slot.add_response_request(response, request)
        # def finish_scraping(_):
        #     slot.finish_response(response, request)
        #     self._check_if_closing(spider, slot)
        #     self._scrape_next(spider, slot)
        #     return _
        # dfd.addBoth(finish_scraping)
        # dfd.addErrback(
        #     lambda f: logger.error('Scraper bug processing %(request)s',
        #                            {'request': request},
        #                            exc_info=failure_to_exc_info(f),
        #                            extra={'spider': spider}))
        # self._scrape_next(spider, slot)
