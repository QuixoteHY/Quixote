# -*- coding: utf-8 -*-

# Quixote settings for demo project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#

BOT_NAME = 'quixote'

SPIDER_MODULES = ['test.test_spider.test']
NEWSPIDER_MODULE = 'test.test_spider.test'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'demo (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Quixote (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See
#SPIDER_MIDDLEWARES = {
#    'demo.middlewares.DemoSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See
#DOWNLOADER_MIDDLEWARES = {
#    'demo.middlewares.DemoDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See
#EXTENSIONS = {
#    'quixote.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See
ITEM_PIPELINES = {
   'test.test_spider.test.test_pipeline.TestPipeline': 300,
   'test.test_spider.test.test_pipeline.TestPipeline2': 400,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Quixote should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'quixote.extensions.httpcache.FilesystemCacheStorage'
