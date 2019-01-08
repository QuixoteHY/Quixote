# -*- coding:utf-8 -*-
# @Time     : 2018-12-31 21:47
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe : 引擎

import types
import time
import logging
import functools

import asyncio

from quixote import loop
from quixote.protocol.request import Request
from quixote.protocol.response import Response
from quixote.downloader import Downloader
from quixote.exception import NoCallbackError, NoRequestInQueue
from quixote.utils.misc import load_object

logger = logging.getLogger(__name__)


class CallLaterOnce(object):
    def __init__(self, func, *a, **kw):
        self._func = func
        self._a = a
        self._kw = kw
        self._call = None

    def schedule(self, delay=1):
        if self._call is None:
            self._call = loop.call_later(delay, self)

    def cancel(self):
        if self._call:
            self._call.cancel()

    def __call__(self):
        self._call = None
        return self._func(*self._a, **self._kw)


class Heart(object):
    def __init__(self, start_requests, next_call, scheduler):
        self.start_requests = iter(start_requests)
        self.next_call = next_call
        self.scheduler = scheduler

    def _heartbeat(self, interval):
        self.next_call.schedule()
        loop.call_later(interval, self._heartbeat, interval)

    def start_heartbeat(self, interval):
        self._heartbeat(interval)


class Engine(object):
    def __init__(self, starter):
        self.starter = starter
        self.settings = starter.settings
        self.loop = None
        self.spider = None
        self.scheduler = None
        self.heart = None
        self.scheduler_class = load_object(self.settings['SCHEDULER'])
        self.running = False
        self.crawling = []
        self.max = 5

    def get_response(self, content, request):
        response = Response(content, request)
        if request.callback:
            gen = request.callback(response)
            if isinstance(gen, types.GeneratorType):
                for req in gen:
                    if isinstance(req, Request):
                        self.scheduler.push_request(req)
                    elif isinstance(req, (str, bytes)):
                        print(req)
                    else:
                        raise TypeError('type of the request callback must be a Request or a str or a bytes, '
                                        'got %s' % type(req).__name__)
        else:
            raise NoCallbackError('No callback function in request')

    def _next_request(self, spider):
        if not self.heart:
            return
        heart = self.heart
        while True:
            if not self._next_request_from_scheduler(spider):
                break
        if heart.start_requests:
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

    def _next_request_from_scheduler(self, spider):
        heart = self.heart
        request = heart.scheduler.pop_request()
        if not request:
            return
        asyncio.run_coroutine_threadsafe(self._download(request, spider), loop)

    def crawl(self, request, spider):
        assert spider in [self.spider], "Spider %r not opened when crawling: %s" % (spider.name, request)
        self.heart.scheduler.push_request(request)
        self.heart.next_call.schedule()

    async def _download(self, request, spider):
        try:
            print('Waiting {}'.format(request.url))
            await asyncio.sleep(3)
            print('Done after {}s'.format(request.url))
            request.callback('url: '+request.url)
            return 'url: '+request.url
        except Exception as e:
            print(e)

    def _handle_downloader_output(self, response, request, spider):
        print(response)

    def start(self, spider):
        self.spider = spider
        next_call = CallLaterOnce(self._next_request, spider)
        scheduler = self.scheduler_class.from_starter(self.starter)
        start_requests = self.spider.start_requests()
        self.heart = Heart(start_requests, next_call, scheduler)
        self.heart.start_heartbeat(5)
        asyncio.set_event_loop(loop)
        loop.run_forever()

    def test(self):
        self.running = True
        while True:
            try:
                request = self.scheduler.pop_request()
                if request:
                    asyncio.run_coroutine_threadsafe(self.do_some_work(6, request.url), loop)
                else:
                    raise NoRequestInQueue('NoRequestInQueue')
            except NoRequestInQueue as e:
                print(e)
                time.sleep(10)

    @staticmethod
    async def do_some_work(x, url):
        print('Waiting {}'.format(url))
        await asyncio.sleep(x)
        print('Done after {}s'.format(url))
        return 'url: '+url
