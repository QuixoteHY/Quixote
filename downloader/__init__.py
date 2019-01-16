# -*- coding:utf-8 -*-
# @Time     : 2018-12-31 22:55
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe : 下载器

import asyncio

from quixote.downloader.download_handlers import DownloadHandlers


class Downloader(object):

    def __init__(self, starter):
        self.settings = starter.settings
        self.slots = {}
        self.active = set()
        self.handlers = DownloadHandlers(starter)
        self.total_concurrency = self.settings['CONCURRENT_REQUESTS']
        self.domain_concurrency = self.settings['CONCURRENT_REQUESTS_PER_DOMAIN']
        self.ip_concurrency = self.settings['CONCURRENT_REQUESTS_PER_IP']
        self.randomize_delay = self.settings['RANDOMIZE_DOWNLOAD_DELAY']
        self.middleware = None  # DownloaderMiddlewareManager.from_crawler(crawler)
        # self._slot_gc_loop = task.LoopingCall(self._slot_gc)
        # self._slot_gc_loop.start(60)

    async def close(self):
        await self.handlers.close()

    async def fetch(self, request, spider):
        self.active.add(request)
        task = self.handlers.download_request(request, spider)
        done, pending = await asyncio.wait({task})
        response = None
        if task in done:
            response = task.result()
        self.active.remove(request)
        return response

    def needs_slowdown(self):
        return len(self.active) >= self.total_concurrency

    def _enqueue_request(self):
        pass
