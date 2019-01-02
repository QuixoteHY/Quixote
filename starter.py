# -*- coding:utf-8 -*-
# @Time     : 2019-01-02 21:13
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe : 爬虫启动器

import logging

import asyncio

from quixote.settings import Settings
from quixote.settings import settings
from quixote.utils.misc import load_object

logger = logging.getLogger(__name__)


class Starter(object):
    def __init__(self, spider_class, settings_class=None):
        if settings_class:
            self.settings = Settings(load_object(settings_class)).get_settings()
        else:
            self.settings = Settings(settings).get_settings()
        self.engine = load_object(self.settings['ENGINE'])
        self.spider = load_object(spider_class)
        self.crawling = False
        print(self.settings)

    def start(self):
        loop = asyncio.get_event_loop()


def main():
    s = Starter('quixote.test.test_spider.TestSpider')


if __name__ == '__main__':
    main()
