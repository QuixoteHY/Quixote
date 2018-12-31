# -*- coding:utf-8 -*-
# @Time     : 2018-12-31 20:13
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe : 对HTTP请求相关操作的封装


class Request(object):
    """
    封装HTTP请求相关信息
    """
    def __init__(self, url, priority=0, callback=None, errback=None):
        self.url = url
        assert isinstance(priority, int), "Request priority not an integer: %r" % priority
        self.priority = 0
        if callback is not None and not callable(callback):
            raise TypeError('callback must be a callable, got %s' % type(callback).__name__)
        if errback is not None and not callable(errback):
            raise TypeError('errback must be a callable, got %s' % type(errback).__name__)
        assert callback or not errback, "Cannot use errback without a callback"
        self.callback = callback
        self.errback = errback
