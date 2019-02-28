# -*- coding:utf-8 -*-
# @Time     : 2019-01-02 21:13
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe : 爬虫启动器

import os
import time
from threading import Thread

import asyncio

from quixote import loop
from quixote.settings import Settings
from quixote.logger import logger
from quixote.extension import ExtensionManager
from quixote.signals.signalmanager import SignalManager
from quixote.utils.misc import load_object

from quixote.utils.schedule_func import CallLaterOnce
import tracemalloc

tracemalloc.start()
project_path = os.path.dirname(__file__)


class CheckMemory(object):
    def __init__(self):
        self.next_call = CallLaterOnce(self._func)

    @staticmethod
    def _func():
        with open(project_path+'/logs/memory.log', 'a') as f:
            snapshot = tracemalloc.take_snapshot()
            top_stats = snapshot.statistics('lineno')
            print('\n[ Top 10 ]')
            f.write(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))}] [ Top 10 ]\n")
            for stat in top_stats[:10]:
                print(stat)
                f.write(str(stat)+'\n')

    def _heartbeat(self, interval):
        self.next_call.schedule()
        loop.call_later(interval, self._heartbeat, interval)

    def start(self, interval):
        self._heartbeat(interval)


class Starter(object):
    def __init__(self, spider_class, settings_class=None, is_check_emmory=False):
        if settings_class:
            self.settings = Settings(load_object(settings_class)).get_settings()
        else:
            from quixote.settings import settings
            self.settings = Settings(settings).get_settings()
        print(self.settings)
        self.engine_class = load_object(self.settings['ENGINE'])
        self.spider_class = load_object(spider_class)
        self.signals = SignalManager()
        self.extensions = ExtensionManager.from_starter(self)
        self.engine = None
        self.spider = None
        self.crawling = False
        self.is_check_emmory = is_check_emmory

    @staticmethod
    def _start():
        asyncio.set_event_loop(loop)
        loop.run_forever()

    def start(self):
        start = int(time.time())
        # t = Thread(target=self._start)
        # t.setDaemon(True)
        # t.start()
        try:
            if self.is_check_emmory:
                cm = CheckMemory()
                cm.start(60)
            self.spider = self._create_spider()
            self.engine = self._create_engine()
            self.engine.start(self.spider)
        except KeyboardInterrupt as e:
            print(e)
            print('total time: '+str(int(time.time())-start))
            loop.stop()

    def _create_spider(self, *args, **kwargs):
        return self.spider_class.from_starter(self, *args, **kwargs)

    def _create_engine(self):
        return self.engine_class(self)


def main():
    s = Starter('quixote.test.test_spider.test_spider.TestSpider', is_check_emmory=True)
    s.start()


if __name__ == '__main__':
    main()
