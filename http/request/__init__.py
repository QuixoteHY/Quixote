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
    def __init__(self, url, callback):
        self.url = url
        self.callback = callback
        self.priority = 0
