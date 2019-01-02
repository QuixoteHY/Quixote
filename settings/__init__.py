# -*- coding:utf-8 -*-
# @Time     : 2018-12-31 19:51
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe : 配置文件

import copy


class Settings(object):

    def __init__(self, settings):
        self.settings = dict()
        self.settings['ENGINE'] = settings.ENGINE
        self.settings['SCHEDULER'] = settings.SCHEDULER
        self.settings['REQUEST_FILTER_CLASS'] = settings.REQUEST_FILTER_CLASS

    def get_settings(self):
        return self.settings

    def copy(self):
        return copy.deepcopy(self.settings)
