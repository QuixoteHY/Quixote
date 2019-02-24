# -*- coding:utf-8 -*-
# @Time     : 2019-01-20 21:35
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe :

from collections import defaultdict
import pprint

from quixote.item import BaseItem
from quixote.logger import logger
from quixote.exception.exceptions import NotConfigured, DropItem
from quixote.utils.misc import load_object


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
    def from_settings(cls, settings, starter=None):
        mwlist = cls._get_middleware_list_from_settings(settings)
        middlewares = []
        enabled = []
        for clspath in mwlist:
            try:
                mwcls = load_object(clspath)
                if starter and hasattr(mwcls, 'from_starter'):
                    mw = mwcls.from_starter(starter)
                elif hasattr(mwcls, 'from_settings'):
                    mw = mwcls.from_settings(settings)
                else:
                    mw = mwcls()
                middlewares.append(mw)
                enabled.append(clspath)
            except NotConfigured as e:
                if e.args:
                    clsname = clspath.split('.')[-1]
                    logger.warning("Disabled %(clsname)s: %(eargs)s", {'clsname': clsname, 'eargs': e.args[0]},
                                   extra={'starter': starter})
        logger.info("Enabled %(componentname)ss:\n%(enabledlist)s",
                    {'componentname': cls.component_name, 'enabledlist': pprint.pformat(enabled)},
                    extra={'starter': starter})
        return cls(*middlewares)

    @classmethod
    def from_starter(cls, starter):
        return cls.from_settings(starter.settings, starter)

    def _add_middleware(self, mw):
        if hasattr(mw, 'open_spider'):
            self.methods['open_spider'].append(mw.open_spider)
        if hasattr(mw, 'close_spider'):
            self.methods['close_spider'].insert(0, mw.close_spider)

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def _process_chain(self, method_name, item, spider):
        res = True
        for method in self.methods[method_name]:
            try:
                item = method(item, spider)
                if not isinstance(item, (BaseItem, dict)):
                    raise DropItem('DropItem: %s do not return BaseItem or dict' % method_name)
            except DropItem as e:
                logger.info('DropItem: %s' % e)
                res = False
                break
        return res
