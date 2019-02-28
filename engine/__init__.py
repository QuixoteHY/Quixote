# -*- coding:utf-8 -*-
# @Time     : 2018-12-31 21:47
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe : 引擎

import asyncio

from pydispatch import dispatcher

from quixote import loop
from quixote.protocol import Request, Response
from quixote.scraper import Scraper
from quixote.signals import engine_started
from quixote.logger import logger
from quixote.utils.misc import load_object
from quixote.utils.schedule_func import CallLaterOnce


class Heart(object):
    def __init__(self, start_requests, next_call, scheduler):
        self.start_requests = iter(start_requests)
        self.next_call = next_call
        self.scheduler = scheduler

    def _heartbeat(self, interval):
        self.next_call.schedule()
        loop.call_later(interval, self._heartbeat, interval)

    def start(self, interval):
        self._heartbeat(interval)


class Engine(object):
    def __init__(self, starter):
        self.starter = starter
        self.settings = starter.settings
        self.signals = starter.signals
        self.loop = None
        self.spider = None
        self.scheduler = None
        self.scraper = Scraper(starter)
        self.heart = None
        self.scheduler_class = load_object(self.settings['SCHEDULER'])
        downloader_class = load_object(self.settings['DOWNLOADER'])
        self.downloader = downloader_class(starter)
        self.running = False
        self.crawling = []
        self.max = 5

    def _next_request(self, spider):
        if not self.heart:
            return
        heart = self.heart
        while not self._needs_slowdown():
            if not self._next_request_from_scheduler(spider):
                break
        if heart.start_requests and not self._needs_slowdown():
            try:
                request = next(heart.start_requests)
            except StopIteration:
                heart.start_requests = None
            except Exception as e:
                heart.start_requests = None
                logger.error('Error while obtaining start requests', exc_info=True,
                             extra={'spider': spider, 'exc_info': str(e)})
            else:
                self.crawl(request, spider)

    def _needs_slowdown(self):
        return self.downloader.needs_slowdown()

    def _next_request_from_scheduler(self, spider):
        heart = self.heart
        request = heart.scheduler.pop_request()
        if not request:
            return False
        asyncio.run_coroutine_threadsafe(self._download(request, spider), loop)
        return True

    async def _download(self, request, spider):
        try:
            response = await self.downloader.fetch(request, spider)
            assert isinstance(response, (Response, Request))
            # b = isinstance(response, Response)
            # a = isinstance(response, HtmlResponse)
            if isinstance(response, Response):
                response.request = request
            self.heart.next_call.schedule()
            self._handle_downloader_output(response, request, spider)
        except Exception as e:
            print(logger.exception(e))
        finally:
            self.heart.next_call.schedule()

    def _handle_downloader_output(self, response, request, spider):
        assert isinstance(response, (Request, Response)), response
        if isinstance(response, Request):
            self.crawl(response, spider)
            return
        # self.scraper.enqueue_scrape(response, request, spider)
        # self.scraper.enqueue_scrape2(response, request, spider)
        # loop.call_later(0, self.scraper.enqueue_scrape2, response, request, spider)
        # loop.call_later(2, self.scraper.enqueue_scrape2, response, request, spider)
        loop.call_later(1, self.scraper.enqueue_scrape2, response, request, spider)
        # for item_or_request in request.callback(response):
        #     print('Parsed {}'.format(item_or_request.decode()))

    def crawl(self, request, spider):
        assert spider in [self.spider], "Spider %r not opened when crawling: %s" % (spider.name, request)
        self.heart.scheduler.push_request(request)
        self.heart.next_call.schedule()

    def start(self, spider):
        first_send = ()
        # self.signals.send(engine_started, first_send)
        dispatcher.send(signal=engine_started, sender=first_send)
        self.spider = spider
        self.before_start_requests(self.spider)
        next_call = CallLaterOnce(self._next_request, spider)
        scheduler = self.scheduler_class.from_starter(self.starter)
        # start_requests = self.spider.start_requests()
        start_requests = self.scraper.spidermw.process_start_requests(self.spider.start_requests(), spider)
        self.heart = Heart(start_requests, next_call, scheduler)
        self.scraper.open_spider(spider)
        self.heart.next_call.schedule()
        self.heart.start(5)
        asyncio.set_event_loop(loop)
        loop.run_forever()

    def before_start_requests(self, spider):
        async def task(_request, _spider):
            try:
                response = await self.downloader.fetch(_request, _spider)
                if not isinstance(response, Response):
                    logger.error('The Download data was not a Response object')
                    return
                for item in _request.callback(response):
                    print(item)
            except Exception as e:
                print(logger.exception(e))
        for request in spider.before_start_requests():
            loop.run_until_complete(task(request, spider))
