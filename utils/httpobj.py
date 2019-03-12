# -*- coding:utf-8 -*-
# @Time     : 2019-01-15 22:15
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe :

import weakref

from six.moves.urllib.parse import urlparse

_urlparse_cache = weakref.WeakKeyDictionary()


def urlparse_cached(request_or_response):
    if request_or_response not in _urlparse_cache:
        _urlparse_cache[request_or_response] = urlparse(request_or_response.url)
    return _urlparse_cache[request_or_response]
