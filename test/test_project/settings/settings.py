
import numbers
from operator import itemgetter

import six

from scrapy.settings import BaseSettings
from scrapy.utils.deprecate import update_classpath
from scrapy.utils.python import without_none_values


def build_component_list(compdict, custom=None, convert=update_classpath):
    """Compose a component list from a { class: order } dictionary."""

    def _check_components(complist):
        if len({convert(c) for c in complist}) != len(complist):
            raise ValueError('Some paths in {!r} convert to the same object, '
                             'please update your settings'.format(complist))

    def _map_keys(compdict):
        if isinstance(compdict, BaseSettings):
            compbs = BaseSettings()
            for k, v in six.iteritems(compdict):
                prio = compdict.getpriority(k)
                if compbs.getpriority(convert(k)) == prio:
                    raise ValueError('Some paths in {!r} convert to the same '
                                     'object, please update your settings'
                                     ''.format(list(compdict.keys())))
                else:
                    compbs.set(convert(k), v, priority=prio)
            return compbs
        else:
            _check_components(compdict)
            return {convert(k): v for k, v in six.iteritems(compdict)}

    def _validate_values(compdict):
        """Fail if a value in the components dict is not a real number or None."""
        for name, value in six.iteritems(compdict):
            if value is not None and not isinstance(value, numbers.Real):
                raise ValueError('Invalid value {} for component {}, please provide ' \
                                 'a real number or None instead'.format(value, name))

    # BEGIN Backwards compatibility for old (base, custom) call signature
    if isinstance(custom, (list, tuple)):
        _check_components(custom)
        return type(custom)(convert(c) for c in custom)

    if custom is not None:
        compdict.update(custom)
    # END Backwards compatibility

    _validate_values(compdict)
    compdict = without_none_values(_map_keys(compdict))
    return [k for k, v in sorted(six.iteritems(compdict), key=itemgetter(1))]


DOWNLOADER_MIDDLEWARES_BASE = {
    # Engine side
    'scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware': 100,
    'scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware': 300,
    'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware': 350,
    'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware': 400,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 500,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 550,
    'scrapy.downloadermiddlewares.ajaxcrawl.AjaxCrawlMiddleware': 500,
    'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware': 580,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 590,
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': 100,
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': 700,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 750,
    'scrapy.downloadermiddlewares.stats.DownloaderStats': None,
    'aaaascrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': 900,
    # Downloader side
}

aa = build_component_list(DOWNLOADER_MIDDLEWARES_BASE)
for i in aa:
    print(i)
