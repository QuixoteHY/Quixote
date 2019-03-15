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

        self.settings['SPIDER_LOADER_CLASS'] = settings.SPIDER_LOADER_CLASS
        self.settings['SPIDER_LOADER_WARN_ONLY'] = settings.SPIDER_LOADER_WARN_ONLY

        self.settings['DOWNLOAD_HANDLERS'] = settings.DOWNLOAD_HANDLERS_BASE
        if settings.DOWNLOAD_HANDLERS:
            self.settings['DOWNLOAD_HANDLERS'].update(settings.DOWNLOAD_HANDLERS)

        self.settings['DOWNLOADER_MIDDLEWARES'] = settings.DOWNLOADER_MIDDLEWARES_BASE
        if settings.DOWNLOADER_MIDDLEWARES:
            self.settings['DOWNLOADER_MIDDLEWARES'].update(settings.DOWNLOADER_MIDDLEWARES)

        self.settings['HTTPCACHE_ENABLED'] = settings.HTTPCACHE_ENABLED
        self.settings['HTTPCACHE_POLICY'] = settings.HTTPCACHE_POLICY
        self.settings['HTTPCACHE_STORAGE'] = settings.HTTPCACHE_STORAGE
        self.settings['HTTPCACHE_IGNORE_MISSING'] = settings.HTTPCACHE_IGNORE_MISSING
        self.settings['HTTPCACHE_DIR'] = settings.HTTPCACHE_DIR
        self.settings['HTTPCACHE_EXPIRATION_SECS'] = settings.HTTPCACHE_EXPIRATION_SECS
        self.settings['HTTPCACHE_ALWAYS_STORE'] = settings.HTTPCACHE_ALWAYS_STORE
        self.settings['HTTPCACHE_IGNORE_HTTP_CODES'] = settings.HTTPCACHE_IGNORE_HTTP_CODES
        self.settings['HTTPCACHE_IGNORE_SCHEMES'] = settings.HTTPCACHE_IGNORE_SCHEMES
        self.settings['HTTPCACHE_IGNORE_RESPONSE_CACHE_CONTROLS'] = settings.HTTPCACHE_IGNORE_RESPONSE_CACHE_CONTROLS
        self.settings['HTTPCACHE_DBM_MODULE'] = settings.HTTPCACHE_DBM_MODULE
        self.settings['HTTPCACHE_GZIP'] = settings.HTTPCACHE_GZIP

        self.settings['COOKIES_ENABLED'] = settings.COOKIES_ENABLED
        self.settings['COOKIES_DEBUG'] = settings.COOKIES_DEBUG

        self.settings['DEFAULT_REQUEST_HEADERS'] = settings.DEFAULT_REQUEST_HEADERS

        self.settings['ITEM_PROCESSOR'] = settings.ITEM_PROCESSOR
        self.settings['CONCURRENT_ITEMS'] = settings.CONCURRENT_ITEMS
        self.settings['ITEM_PIPELINES'] = settings.ITEM_PIPELINES_BASE
        if settings.ITEM_PIPELINES:
            self.settings['ITEM_PIPELINES'].update(settings.ITEM_PIPELINES)

        self.settings['SPIDER_MIDDLEWARES'] = settings.SPIDER_MIDDLEWARES_BASE
        if settings.SPIDER_MIDDLEWARES:
            self.settings['SPIDER_MIDDLEWARES'].update(settings.SPIDER_MIDDLEWARES)
        self.settings['URLLENGTH_LIMIT'] = settings.URLLENGTH_LIMIT
        self.settings['HTTPERROR_ALLOW_ALL'] = settings.HTTPERROR_ALLOW_ALL
        self.settings['HTTPERROR_ALLOWED_CODES'] = settings.HTTPERROR_ALLOWED_CODES

        self.settings['EXTENSIONS'] = settings.EXTENSIONS_BASE
        if settings.EXTENSIONS:
            self.settings['EXTENSIONS'].update(settings.EXTENSIONS)

        self.settings['TELNETCONSOLE_ENABLED'] = settings.TELNETCONSOLE_ENABLED
        self.settings['TELNETCONSOLE_PORT'] = settings.TELNETCONSOLE_PORT
        self.settings['TELNETCONSOLE_HOST'] = settings.TELNETCONSOLE_HOST

        self.settings['STATS_CLASS'] = settings.STATS_CLASS
        self.settings['STATS_DUMP'] = settings.STATS_DUMP

        self.settings['DOWNLOADER_STATS'] = settings.DOWNLOADER_STATS

    def get_settings(self):
        return copy.deepcopy(self.settings)

    def copy(self):
        return copy.deepcopy(self.settings)

    @staticmethod
    def get_dict_from_settings_file(settings):
        settings_dict = dict()
        if hasattr(settings, 'BOT_NAME'):
            settings_dict['BOT_NAME'] = settings.BOT_NAME
        if hasattr(settings, 'SPIDER_MODULES'):
            settings_dict['SPIDER_MODULES'] = settings.SPIDER_MODULES
        if hasattr(settings, 'NEWSPIDER_MODULE'):
            settings_dict['NEWSPIDER_MODULE'] = settings.NEWSPIDER_MODULE
        if hasattr(settings, 'ITEM_PIPELINES'):
            # settings_dict['ITEM_PIPELINES'] = settings.ITEM_PIPELINES
            settings_dict['ITEM_PIPELINES'] = {settings.BOT_NAME+'.'+k: v for k, v in settings.ITEM_PIPELINES.items()}
        if hasattr(settings, 'SPIDER_MIDDLEWARES'):
            # settings_dict['SPIDER_MIDDLEWARES'] = settings.SPIDER_MIDDLEWARES
            settings_dict['SPIDER_MIDDLEWARES'] = {
                settings.BOT_NAME+'.'+k: v for k, v in settings.SPIDER_MIDDLEWARES.items()}
        return settings_dict
