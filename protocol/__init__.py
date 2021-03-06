# -*- coding:utf-8 -*-
# @Time     : 2018-12-31 20:10
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe : 对HTTP相关操作的封装

from quixote.protocol.request import Request
from quixote.protocol.request.form import FormRequest
from quixote.protocol.response import Response
from quixote.protocol.response.text import TextResponse
from quixote.protocol.response.html import HtmlResponse
from quixote.protocol.response.xml import XmlResponse
from quixote.protocol.headers import Headers

from quixote.protocol.telnet.telnetserver import TelnetServer
