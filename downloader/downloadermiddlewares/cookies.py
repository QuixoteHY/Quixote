# -*- coding:utf-8 -*-
# @Time     : 2019-01-20 21:43
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe :

import six
from collections import defaultdict

from quixote.logger import logger
from quixote.exceptions import NotConfigured
from quixote.protocol import Response
from quixote.protocol.cookies import CookieJar
from quixote.utils.python import to_native_str


class CookiesMiddleware(object):
    """This middleware enables working with sites that need cookies"""

    def __init__(self, debug=False):
        self.jars = defaultdict(CookieJar)
        self.debug = debug

    @classmethod
    def from_starter(cls, starter):
        if not starter.settings['COOKIES_ENABLED']:
            raise NotConfigured
        return cls(starter.settings['COOKIES_DEBUG'])

    async def process_request(self, request, spider):
        if request.meta.get('dont_merge_cookies', False):
            return
        cookiejarkey = request.meta.get("cookiejar")
        jar = self.jars[cookiejarkey]
        cookies = self._get_request_cookies(jar, request)
        for cookie in cookies:
            jar.set_cookie_if_ok(cookie, request)
        # set Cookie header
        request.headers.pop('Cookie', None)
        jar.add_cookie_header(request)
        self._debug_cookie(request, spider)

    def process_response(self, request, response, spider):
        if request.meta.get('dont_merge_cookies', False):
            return response
        # extract cookies from Set-Cookie and drop invalid/expired cookies
        cookiejarkey = request.meta.get("cookiejar")
        jar = self.jars[cookiejarkey]
        jar.extract_cookies(response, request)
        self._debug_set_cookie(response, spider)
        return response

    def _debug_cookie(self, request, spider):
        if self.debug:
            cl = [to_native_str(c, errors='replace')
                  for c in request.headers.getlist('Cookie')]
            if cl:
                cookies = "\n".join("Cookie: {}\n".format(c) for c in cl)
                msg = "Sending cookies to: {}\n{}".format(request, cookies)
                logger.debug(msg, extra={'spider': spider})

    def _debug_set_cookie(self, response, spider):
        if self.debug:
            cl = [to_native_str(c, errors='replace')
                  for c in response.headers.getlist('Set-Cookie')]
            if cl:
                cookies = "\n".join("Set-Cookie: {}\n".format(c) for c in cl)
                msg = "Received cookies from: {}\n{}".format(response, cookies)
                logger.debug(msg, extra={'spider': spider})

    @staticmethod
    def _format_cookie(cookie):
        # build cookie string
        cookie_str = '%s=%s' % (cookie['name'], cookie['value'])
        if cookie.get('path', None):
            cookie_str += '; Path=%s' % cookie['path']
        if cookie.get('domain', None):
            cookie_str += '; Domain=%s' % cookie['domain']
        return cookie_str

    def _get_request_cookies(self, jar, request):
        if isinstance(request.cookies, dict):
            cookie_list = [{'name': k, 'value': v} for k, v in six.iteritems(request.cookies)]
        else:
            cookie_list = request.cookies
        cookies = [self._format_cookie(x) for x in cookie_list]
        headers = {'Set-Cookie': cookies}
        response = Response(request.url, headers=headers)
        return jar.make_cookies(response, request)
