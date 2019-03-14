# -*- coding:utf-8 -*-
# @Time     : 2018-12-31 20:51
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe : 爬虫基类

from quixote.protocol.request import Request


class Spider(object):
    """
    爬虫基类
    """
    name = None

    def __init__(self, name=None, **kwargs):
        if name is not None:
            self.name = name
        elif not getattr(self, 'name', None):
            raise ValueError("%s must have a name" % type(self).__name__)
        self.__dict__.update(kwargs)
        if not hasattr(self, 'start_urls'):
            self.start_urls = []

    @classmethod
    def from_starter(cls, starter, *args, **kwargs):
        spider = cls(*args, **kwargs)
        spider._set_starter(starter)
        return spider

    def _set_starter(self, starter):
        self.starter = starter
        self.settings = starter.settings

    def before_start_requests(self):
        """目前可用于（后续有其他需求将继续添加并改进相关代码）：
        1、爬虫开始前登录目标网站，目的是将登录信息保存下来
        :return:
        """
        yield

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url)

    def parse(self, response):
        raise NotImplementedError('{}.parse callback is not defined'.format(self.__class__.__name__))
