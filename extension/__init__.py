# -*- coding:utf-8 -*-
# @Time     : 2019-02-28 08:28
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe :

from quixote.logger import logger
from quixote.exceptions import ErrorSettings
from quixote.middleware import MiddlewareManager


class ExtensionManager(MiddlewareManager):
    component_name = 'extension'

    @classmethod
    def _get_middleware_list_from_settings(cls, settings):
        mw_dict = settings['EXTENSIONS']
        preprocess_mw_dict = dict()
        for k, v in mw_dict.items():
            if not v:
                continue
            if isinstance(v, int):
                preprocess_mw_dict[k] = v
            else:
                logger.error('There is an error in your settings file.\nThe variable EXTENSIONS error.')
                raise ErrorSettings('Settings EXTENSIONS error: '+str((k, v)))
        sorted_mw_list = sorted(preprocess_mw_dict.items(), key=lambda x: x[1], reverse=False)
        mw_list = list()
        for mw in sorted_mw_list:
            mw_list.append(mw[0])
        return mw_list
