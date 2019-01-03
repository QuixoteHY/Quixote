# -*- coding:utf-8 -*-
# @Time     : 2018-12-31 20:17
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe : 对HTTP响应相关操作的封装


class Response(object):
    """
    封装HTTP响应相关信息
    """
    def __init__(self, content, request):
        self.content = content
        self.request = request
