# -*- coding:utf-8 -*-
# @Time     : 2018-12-31 22:55
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe : 下载器

import asyncio
import aiohttp

from quixote.protocol.response import Response


class Downloader(object):

    def __init__(self, starter):
        self.settings = starter.settings
        self.slots = {}
        self.active = set()
        self.handlers = None  # DownloadHandlers(crawler)
        self.total_concurrency = self.settings['CONCURRENT_REQUESTS']
        self.domain_concurrency = self.settings['CONCURRENT_REQUESTS_PER_DOMAIN']
        self.ip_concurrency = self.settings['CONCURRENT_REQUESTS_PER_IP']
        self.randomize_delay = self.settings['RANDOMIZE_DOWNLOAD_DELAY']
        self.middleware = None  # DownloaderMiddlewareManager.from_crawler(crawler)
        # self._slot_gc_loop = task.LoopingCall(self._slot_gc)
        # self._slot_gc_loop.start(60)

    async def fetch(self, request, spider):
        self.active.add(request)
        response = await self.download(request)
        self.active.remove(request)
        return response

    def needs_slowdown(self):
        return len(self.active) >= self.total_concurrency

    def _enqueue_request(self):
        pass

    @staticmethod
    async def download(request):
        print('Downloading {}'.format(request.url))
        await asyncio.sleep(1)
        return Response('url: '+request.url, request)

    @staticmethod
    async def get(url, headers=None, cookies=None, proxy=None, timeout=10):
        if cookies:
            session = aiohttp.ClientSession(cookies=cookies)
        else:
            session = aiohttp.ClientSession()
        if proxy:
            response = await session.get(url, headers=headers, proxy=proxy, timeout=timeout)
        else:
            response = await session.get(url, headers=headers, timeout=timeout)
        await session.close()
        return response

    @staticmethod
    async def post(url, headers=None, data=None, cookies=None, proxy=None, timeout=10):
        if cookies:
            session = aiohttp.ClientSession(cookies=cookies)
        else:
            session = aiohttp.ClientSession()
        if proxy:
            response = await session.post(url, headers=headers, data=data, proxy=proxy, timeout=timeout)
        else:
            response = await session.post(url, headers=headers, data=data, timeout=timeout)
        await session.close()
        return response
