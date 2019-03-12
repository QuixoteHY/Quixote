# -*- coding:utf-8 -*-
# @Time     : 2019-01-19 00:28
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe :
"""
This module implements the HtmlResponse class which adds encoding
discovering through HTML encoding declarations to the TextResponse class.
See documentation in docs/topics/request-response.rst
"""

from quixote.protocol.response.text import TextResponse


class HtmlResponse(TextResponse):
    pass
