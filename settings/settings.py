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

CONCURRENT_REQUESTS = 200
CONCURRENT_REQUESTS_PER_DOMAIN = 8
CONCURRENT_REQUESTS_PER_IP = 0

RANDOMIZE_DOWNLOAD_DELAY = True
