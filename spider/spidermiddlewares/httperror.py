# -*- coding:utf-8 -*-
# @Time     : 2019-02-24 16:35
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe :

from quixote.logger import logger
from quixote.exceptions import IgnoreRequest


class HttpError(IgnoreRequest):
    """A non-200 response was filtered"""
    def __init__(self, response, *args, **kwargs):
        self.response = response
        super(HttpError, self).__init__(*args, **kwargs)


class HttpErrorMiddleware(object):
    def __init__(self, settings):
        self.handle_http_status_all = settings['HTTPERROR_ALLOW_ALL']
        self.handle_http_status_list = settings['HTTPERROR_ALLOWED_CODES']

    @classmethod
    def from_starter(cls, starter):
        return cls(starter.settings)

    def process_spider_input(self, response, spider):
        # response.url = response.url + '_200'
        if 200 <= response.status < 300:
            return
        meta = response.meta
        if 'handle_http_status_all' in meta:
            return
        if 'handle_http_status_list' in meta:
            allowed_statuses = meta['handle_http_status_list']
        elif self.handle_http_status_all:
            return
        else:
            allowed_statuses = getattr(spider, 'handle_http_status_list', self.handle_http_status_list)
        if response.status in allowed_statuses:
            return
        raise HttpError(response, 'Ignoring non-200 response')

    def process_spider_exception(self, response, exception, spider):
        if isinstance(exception, HttpError):
            # spider.starter.stats.inc_value('httperror/response_ignored_count')
            # spider.starter.stats.inc_value(
            #     'httperror/response_ignored_status_count/%s' % response.status
            # )
            logger.info(
                "Ignoring response %(response)r: HTTP status code is not handled or not allowed",
                {'response': response}, extra={'spider': spider},
            )
            return []
