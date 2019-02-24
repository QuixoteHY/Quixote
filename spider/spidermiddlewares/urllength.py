# -*- coding:utf-8 -*-
# @Time     : 2019-02-23 21:54
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe :

from quixote.protocol import Request
from quixote.logger import logger
from quixote.exception.exceptions import NotConfigured


class UrlLengthMiddleware(object):
    def __init__(self, max_length):
        self.max_length = max_length

    @classmethod
    def from_settings(cls, settings):
        max_length = settings['URLLENGTH_LIMIT']
        if not max_length:
            raise NotConfigured
        return cls(max_length)

    def process_spider_output(self, response, result, spider):
        def _filter(request):
            if isinstance(request, Request) and len(request.url) > self.max_length:
                logger.warn("Ignoring link (url length > %(max_length)d): %(url)s ",
                            {'max_length': self.max_length, 'url': request.url},
                            extra={'spider': spider})
                return False
            else:
                return True
        return (r for r in result or () if _filter(r))
