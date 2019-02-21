# -*- coding:utf-8 -*-
# @Time     : 2019-02-21 09:20
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe :

from quixote.middleware import MiddlewareManager


class ItemPipelineManager(object):
    def __init__(self):
        pass

    @classmethod
    def from_starter(cls, starter):
        return cls()

    def open_spider(self, spider):
        pass
