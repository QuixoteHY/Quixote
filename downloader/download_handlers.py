# -*- coding:utf-8 -*-
# @Time     : 2019-01-15 22:09
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe :

import six

from quixote.exception.download_handlers import NotConfigured, NotSupportedURLScheme
from quixote.logger import logger
from quixote.utils.misc import load_object
from quixote.utils.httpobj import urlparse_cached


class DownloadHandlers(object):
    def __init__(self, starter):
        self._starter = starter
        self._schemes = {}  # stores acceptable schemes on instancing
        self._handlers = {}  # stores instanced handlers for schemes
        self._not_configured = {}  # remembers failed handlers
        handlers = starter.settings['DOWNLOAD_HANDLERS']
        for scheme, class_path in six.iteritems(handlers):
            self._schemes[scheme] = class_path

    async def close(self):
        for handler in self._handlers:
            await handler.close()

    def _get_handler(self, scheme):
        if scheme in self._handlers:
            return self._handlers[scheme]
        if scheme in self._not_configured:
            return None
        if scheme not in self._schemes:
            self._not_configured[scheme] = 'no handler available for that scheme'
            return None
        path = self._schemes[scheme]
        try:
            download_handler = load_object(path)
            dh = download_handler(self._starter.settings)
        except NotConfigured as e:
            self._not_configured[scheme] = str(e)
            return None
        except Exception as e:
            logger.error('Loading "%(class_path)s" for scheme "%(scheme)s"', {"class_path": path, "scheme": scheme},
                         exc_info=True,  extra={'crawler': self._starter})
            self._not_configured[scheme] = str(e)
            return None
        else:
            self._handlers[scheme] = dh
        return self._handlers[scheme]

    def download_request(self, request, spider):
        scheme = urlparse_cached(request).scheme
        handler = self._get_handler(scheme)
        if not handler:
            raise NotSupportedURLScheme("Unsupported URL scheme '%s': %s" % (scheme, self._not_configured[scheme]))
        return handler.download_request(request, spider)
