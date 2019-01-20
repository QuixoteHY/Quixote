# -*- coding:utf-8 -*-
# @Time     : 2019-01-20 21:35
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe :

from collections import defaultdict
import logging
import pprint

from quixote.exception.exceptions import NotConfigured
from quixote.utils.misc import load_object

logger = logging.getLogger(__name__)


class MiddlewareManager(object):
    component_name = 'base middleware'

    def __init__(self, *middlewares):
        self.middlewares = middlewares
        self.methods = defaultdict(list)
        for mw in middlewares:
            self._add_middleware(mw)

    @classmethod
    def _get_middleware_list_from_settings(cls, settings):
        raise NotImplementedError

    @classmethod
    def from_settings(cls, settings, crawler=None):
        mwlist = cls._get_middleware_list_from_settings(settings)
        middlewares = []
        enabled = []
        for clspath in mwlist:
            try:
                mwcls = load_object(clspath)
                if crawler and hasattr(mwcls, 'from_crawler'):
                    mw = mwcls.from_crawler(crawler)
                elif hasattr(mwcls, 'from_settings'):
                    mw = mwcls.from_settings(settings)
                else:
                    mw = mwcls()
                middlewares.append(mw)
                enabled.append(clspath)
            except NotConfigured as e:
                if e.args:
                    clsname = clspath.split('.')[-1]
                    logger.warning("Disabled %(clsname)s: %(eargs)s",
                                   {'clsname': clsname, 'eargs': e.args[0]},
                                   extra={'crawler': crawler})
        logger.info("Enabled %(componentname)ss:\n%(enabledlist)s", {'componentname': cls.component_name,
                                                                     'enabledlist': pprint.pformat(enabled)},
                    extra={'crawler': crawler})
        return cls(*middlewares)

    @classmethod
    def from_crawler(cls, crawler):
        return cls.from_settings(crawler.settings, crawler)

    def _add_middleware(self, mw):
        if hasattr(mw, 'open_spider'):
            self.methods['open_spider'].append(mw.open_spider)
        if hasattr(mw, 'close_spider'):
            self.methods['close_spider'].insert(0, mw.close_spider)
