# -*- coding:utf-8 -*-
# @Time     : 2019-01-02 21:13
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe : 爬虫启动器

import logging
import time
from threading import Thread

import asyncio

from quixote.settings import Settings
from quixote.utils.misc import load_object

logger = logging.getLogger(__name__)


class Starter(object):
    def __init__(self, spider_class, settings_class=None):
        if settings_class:
            self.settings = Settings(load_object(settings_class)).get_settings()
        else:
            from quixote.settings import settings
            self.settings = Settings(settings).get_settings()
        print(self.settings)
        self.engine = load_object(self.settings['ENGINE'])
        self.spider = load_object(spider_class)
        self.crawling = False
        self.now = lambda: time.time()

    @staticmethod
    def _start(loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

    def start(self):
        start = self.now()
        new_loop = asyncio.new_event_loop()
        t = Thread(target=self._start, args=(new_loop,))
        t.setDaemon(True)
        t.start()
        print('TIME: {}'.format(self.now() - start))
        try:
            while True:
                asyncio.run_coroutine_threadsafe(self.do_some_work(6), new_loop)
                asyncio.run_coroutine_threadsafe(self.do_some_work(4), new_loop)
        except KeyboardInterrupt as e:
            print('$$$$$$$$'+str(e))
            new_loop.stop()

    @staticmethod
    async def do_some_work(x):
        print('Waiting {}'.format(x))
        await asyncio.sleep(x)
        print('Done after {}s'.format(x))


def main():
    s = Starter('quixote.test.test_spider.TestSpider')
    s.start()


if __name__ == '__main__':
    main()
