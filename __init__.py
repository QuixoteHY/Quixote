# -*- coding:utf-8 -*-
# @Time     : 2018-12-31 21:18
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe : A crawler framework is based on asyncio.

import asyncio

from quixote.spider import Spider
from quixote.protocol import Request, FormRequest

loop = asyncio.new_event_loop()
