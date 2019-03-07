# -*- coding:utf-8 -*-
# @Time     : 2019-03-07 08:37
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe :

from quixote.exceptions import NotConfigured
from quixote.utils.request import request_httprepr
from quixote.utils.response import response_httprepr
from quixote.utils.python import global_object_name


class DownloaderStats(object):
    def __init__(self, stats):
        self.stats = stats

    @classmethod
    def from_starter(cls, starter):
        if not starter.settings['DOWNLOADER_STATS']:
            raise NotConfigured
        return cls(starter.stats)

    async def process_request(self, request, spider):
        self.stats.inc_value('downloader/request_count', spider=spider)
        self.stats.inc_value('downloader/request_method_count/%s' % request.method, spider=spider)
        reqlen = len(request_httprepr(request))
        self.stats.inc_value('downloader/request_bytes', reqlen, spider=spider)

    def process_response(self, request, response, spider):
        self.stats.inc_value('downloader/response_count', spider=spider)
        self.stats.inc_value('downloader/response_status_count/%s' % response.status, spider=spider)
        reslen = len(response_httprepr(response))
        self.stats.inc_value('downloader/response_bytes', reslen, spider=spider)
        return response

    def process_exception(self, request, exception, spider):
        ex_class = global_object_name(exception.__class__)
        self.stats.inc_value('downloader/exception_count', spider=spider)
        self.stats.inc_value('downloader/exception_type_count/%s' % ex_class, spider=spider)
