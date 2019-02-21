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

        download_handlers = settings.DOWNLOAD_HANDLERS_BASE
        if settings.DOWNLOAD_HANDLERS:
            self.settings['DOWNLOAD_HANDLERS'] = download_handlers.update(settings.DOWNLOAD_HANDLERS)
        else:
            self.settings['DOWNLOAD_HANDLERS'] = download_handlers

        downloader_middlewares = settings.DOWNLOADER_MIDDLEWARES_BASE
        if settings.DOWNLOADER_MIDDLEWARES:
            self.settings['DOWNLOADER_MIDDLEWARES'] = downloader_middlewares.update(settings.DOWNLOADER_MIDDLEWARES)
        else:
            self.settings['DOWNLOADER_MIDDLEWARES'] = downloader_middlewares

        self.settings['COOKIES_ENABLED'] = settings.COOKIES_ENABLED
        self.settings['COOKIES_DEBUG'] = settings.COOKIES_DEBUG

        self.settings['DEFAULT_REQUEST_HEADERS'] = settings.DEFAULT_REQUEST_HEADERS

        self.settings['ITEM_PROCESSOR'] = settings.ITEM_PROCESSOR
        self.settings['CONCURRENT_ITEMS'] = settings.CONCURRENT_ITEMS

    def get_settings(self):
        return copy.deepcopy(self.settings)

    def copy(self):
        return copy.deepcopy(self.settings)
