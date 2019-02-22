# -*- coding:utf-8 -*-
# @Time     : 2018-12-31 19:51
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe : 配置文件

ENGINE = 'quixote.engine.Engine'

SCHEDULER = 'quixote.scheduler.Scheduler'

DOWNLOADER = 'quixote.downloader.Downloader'

REQUEST_FILTER_CLASS = 'None'

CONCURRENT_REQUESTS = 400
CONCURRENT_REQUESTS_PER_DOMAIN = 8
CONCURRENT_REQUESTS_PER_IP = 0

RANDOMIZE_DOWNLOAD_DELAY = True

DOWNLOAD_HANDLERS = {}
DOWNLOAD_HANDLERS_BASE = {
    'http': 'quixote.downloader.download_handler.http_download_handler.HTTPDownloadHandler',
    'https': 'quixote.downloader.download_handler.http_download_handler.HTTPDownloadHandler'
}

DOWNLOADER_MIDDLEWARES = {}
DOWNLOADER_MIDDLEWARES_BASE = {
    'quixote.downloader.downloadermiddlewares.default_headers.DefaultHeadersMiddleware': 400,
    'quixote.downloader.downloadermiddlewares.cookies.CookiesMiddleware': 700,
}
# DOWNLOADER_MIDDLEWARES_BASE = {
#     # Engine side
#     'scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware': 100,
#     'scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware': 300,
#     'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware': 350,
#     'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware': 400,
#     'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 500,
#     'scrapy.downloadermiddlewares.retry.RetryMiddleware': 550,
#     'scrapy.downloadermiddlewares.ajaxcrawl.AjaxCrawlMiddleware': 560,
#     'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware': 580,
#     'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 590,
#     'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': 600,
#     'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': 700,
#     'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 750,
#     'scrapy.downloadermiddlewares.stats.DownloaderStats': 850,
#     'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': 900,
#     # Downloader side
# }

COOKIES_ENABLED = True
COOKIES_DEBUG = False

DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
}

ITEM_PROCESSOR = 'quixote.scraper.pipelines.ItemPipelineManager'
CONCURRENT_ITEMS = 100
ITEM_PIPELINES = {
    'quixote.test.test_spider.test_pipeline.TestPipeline': 100,
}
ITEM_PIPELINES_BASE = {}
