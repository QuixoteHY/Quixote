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
        self.settings['DOWNLOADER'] = settings.DOWNLOADER

        self.settings['REQUEST_FILTER_CLASS'] = settings.REQUEST_FILTER_CLASS

        self.settings['CONCURRENT_REQUESTS'] = settings.CONCURRENT_REQUESTS
        self.settings['CONCURRENT_REQUESTS_PER_DOMAIN'] = settings.CONCURRENT_REQUESTS_PER_DOMAIN
        self.settings['CONCURRENT_REQUESTS_PER_IP'] = settings.CONCURRENT_REQUESTS_PER_IP

        self.settings['RANDOMIZE_DOWNLOAD_DELAY'] = settings.RANDOMIZE_DOWNLOAD_DELAY

    def get_settings(self):
        return copy.deepcopy(self.settings)

    def copy(self):
        return copy.deepcopy(self.settings)
