# -*- coding:utf-8 -*-
# @Time     : 2018-12-31 19:52
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe : 调度器

import logging
from queue import Queue

from quixote.utils.misc import load_object

logger = logging.getLogger(__name__)


class Scheduler(object):
    """
    调度器
    """
    def __init__(self, request_filter=None):
        self.q = Queue()
        self.rf = request_filter

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        request_filter = load_object(settings['REQUEST_FILTER_CLASS'])
        return cls(request_filter)

    def pop_request(self):
        try:
            request = self.q.get(block=False)
        except Exception as e:
            request = None
            logger.info('No request object in the queue now!\t'+str(e))
        return request

    def push_request(self, request):
        self.q.put(request, block=False)

    def size(self):
        return self.q.qsize()
