# -*- coding:utf-8 -*-
# @Time     : 2019-02-21 09:20
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe :

from quixote.item import BaseItem
from quixote.middleware import MiddlewareManager
from quixote.logger import logger
from quixote.exceptions import DropItem, ErrorSettings


class ItemPipelineManager(MiddlewareManager):
    component_name = 'item pipeline'

    @classmethod
    def _get_middleware_list_from_settings(cls, settings):
        mw_dict = settings['ITEM_PIPELINES']
        preprocess_mw_dict = dict()
        for k, v in mw_dict.items():
            if not v:
                continue
            if isinstance(v, int):
                preprocess_mw_dict[k] = v
            else:
                logger.error('There is an error in your settings file.\nThe variable ITEM_PIPELINES error.')
                raise ErrorSettings('Settings ITEM_PIPELINES error: '+str((k, v)))
        sorted_mw_list = sorted(preprocess_mw_dict.items(), key=lambda x: x[1], reverse=False)
        mw_list = list()
        for mw in sorted_mw_list:
            mw_list.append(mw[0])
        return mw_list

    def _add_middleware(self, pipe):
        super(ItemPipelineManager, self)._add_middleware(pipe)
        if hasattr(pipe, 'process_item'):
            self.methods['process_item'].append(pipe.process_item)

    def process_item(self, item, spider):
        res = True
        for method in self.methods['process_item']:
            try:
                item = method(item, spider)
                if not isinstance(item, (BaseItem, dict)):
                    raise DropItem('DropItem: process_item do not return BaseItem or dict')
            except DropItem as e:
                logger.info('DropItem: %s' % e)
                res = False
                break
        return res
