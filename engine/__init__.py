# -*- coding:utf-8 -*-
# @Time     : 2018-12-31 21:47
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe : 引擎

import types
import time

import asyncio

from quixote.protocol.request import Request
from quixote.protocol.response import Response
from quixote.downloader import Downloader
from quixote.exception import NoCallbackError, NoRequestInQueue
from quixote.utils.misc import load_object


class Engine(object):
    def __init__(self, starter):
        self.starter = starter
        self.settings = starter.settings
        self.loop = None
        self.spider = None
        self.scheduler = None
        self.scheduler_class = load_object(self.settings['SCHEDULER'])
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

    async def _next_request(self):
        if self.scheduler.size() == 0 and len(self.crawling) == 0:
            self._closewait.callback(None)
        if len(self.crawling) >= 5:
            return
        while len(self.crawling) < 5:
            req = self.scheduler.pop_request()
            if not req:
                return
            d = await Downloader.get(req.url.encode('utf-8'))
            self.crawling.append(d)
            d.addCallback(self.get_response, req)

    def open_spider(self, spider, loop):
        self.spider = spider
        self.loop = loop
        self.scheduler = self.scheduler_class.from_starter(self.starter)
        for request in self.spider.start_requests():
            self.scheduler.push_request(request)
        # flag = True
        # while flag:
        #     try:
        #         # req = next(start_requests)
        #         # self.scheduler.push_request(req)
        #         pass
        #     except StopIteration as _:
        #         flag = False

    def start(self):
        while True:
            try:
                request = self.scheduler.pop_request()
                if request:
                    asyncio.run_coroutine_threadsafe(self.do_some_work(6, request.url), self.loop)
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
