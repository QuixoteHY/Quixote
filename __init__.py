# -*- coding:utf-8 -*-
# @Time     : 2018-12-31 21:18
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe : A crawler framework is based on asyncio.

import os

import asyncio

from quixote.spider import Spider
from quixote.protocol import Request, FormRequest
from quixote.item import Item, Field
from quixote.logger import logger

loop = asyncio.new_event_loop()

FRAME_PATH = os.path.dirname(os.path.abspath(__file__))
