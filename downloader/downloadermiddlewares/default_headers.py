# -*- coding:utf-8 -*-
# @Time     : 2019-02-18 20:04
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe : DefaultHeaders downloader middleware

from quixote.utils.python import without_none_values


class DefaultHeadersMiddleware(object):

    def __init__(self, headers):
        self._headers = headers

    @classmethod
    def from_starter(cls, starter):
        headers = without_none_values(starter.settings['DEFAULT_REQUEST_HEADERS'])
        return cls(headers.items())

    async def process_request(self, request, spider):
        for k, v in self._headers:
            request.headers.setdefault(k, v)
