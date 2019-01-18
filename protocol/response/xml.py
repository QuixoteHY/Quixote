# -*- coding:utf-8 -*-
# @Time     : 2019-01-19 00:29
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe :
"""
This module implements the XmlResponse class which adds encoding
discovering through XML encoding declarations to the TextResponse class.
See documentation in docs/topics/request-response.rst
"""

from quixote.protocol.response.text import TextResponse


class XmlResponse(TextResponse):
    pass
