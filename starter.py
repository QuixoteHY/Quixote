# -*- coding:utf-8 -*-
# @Time     : 2019-01-02 21:13
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe : 爬虫启动器

import os
import time

from zope.interface.exceptions import DoesNotImplement
from zope.interface.verify import verifyClass

from quixote import loop
from quixote.settings import Settings
from quixote.logger import logger
from quixote import signals
from quixote.exceptions import QuixoteDeprecationWarning
from quixote.extension import ExtensionManager
from quixote.signals.signalmanager import SignalManager
from quixote.utils.misc import load_object
from quixote.spider.spiderloader import ISpiderLoader

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


def _get_spider_loader(settings):
    """Get SpiderLoader instance from settings"""
    cls_path = settings['SPIDER_LOADER_CLASS']
    loader_cls = load_object(cls_path)
    try:
        verifyClass(ISpiderLoader, loader_cls)
    except DoesNotImplement:
        logger.warn('SPIDER_LOADER_CLASS (previously named SPIDER_MANAGER_CLASS) does not fully implement '
                    'quixote.spider.spiderloader.ISpiderLoader interface. Please add all missing methods to avoid '
                    'unexpected runtime errors.', category=QuixoteDeprecationWarning, stacklevel=2)
    return loader_cls.from_settings(settings)


class Starter(object):
    def __init__(self, spider_name, project_settings=None, is_check_emmory=False):
        from quixote.settings import settings
        self.settings = Settings(settings).get_settings()
        project_settings = Settings.get_dict_from_settings_file(project_settings)
        for s_k, s_v in project_settings.items():
            self.settings[s_k] = s_v
        self.spider_loader = _get_spider_loader(self.settings)
        print(self.settings)
        self.engine_class = load_object(self.settings['ENGINE'])
        # self.spider_class = load_object(spider_class)
        self.spider_class = self.spider_loader.get_spider_by_name(spider_name)
        self.signals = SignalManager()
        self.stats = load_object(self.settings['STATS_CLASS'])(self)
        self.extensions = ExtensionManager.from_starter(self)
        self.engine = None
        self.spider = None
        self.crawling = False
        self.is_check_emmory = is_check_emmory
        self.start_time = None

    def start(self):
        assert not self.crawling, "Crawling already taking place"
        self.crawling = True
        self.start_time = int(time.time())
        try:
            if self.is_check_emmory:
                cm = CheckMemory()
                cm.start(60)
            self.spider = self._create_spider()
            self.engine = self._create_engine()
            self.engine.start(self.spider)
        except KeyboardInterrupt as e:
            logger.info(e)
            self.close('KeyboardInterrupt')
        except Exception as e:
            logger.info(logger.exception(e))
            self.close(str(e))

    def close(self, reason):
        # 必须先与engine关闭
        # self.signals.send(signals.spider_closed, self.engine.spider)
        self.crawling = False
        if self.engine is not None:
            self.engine.close()
        logger.info('total time: '+str(int(time.time())-self.start_time))
        self.stats.close_spider(self.spider, reason=reason)
        loop.stop()

    def _create_spider(self, *args, **kwargs):
        return self.spider_class.from_starter(self, *args, **kwargs)

    def _create_engine(self):
        return self.engine_class(self)


def main():
    """"""
    s = Starter('quixote.test.test_spider.test_spider.TestSpider', is_check_emmory=True)
    s.start()


if __name__ == '__main__':
    main()
