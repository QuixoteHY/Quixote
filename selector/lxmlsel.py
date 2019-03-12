# -*- coding:utf-8 -*-
# @Time     : 2019-01-19 00:32
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe : XPath selectors based on lxml

from quixote.utils.deprecate import create_deprecated_class
from .unified import Selector, SelectorList


__all__ = ['HtmlXPathSelector', 'XmlXPathSelector', 'XPathSelector',
           'XPathSelectorList']


def _xpathselector_css(self, *a, **kw):
    raise RuntimeError('.css() method not available for %s, instantiate scrapy.Selector instead' % type(self).__name__)


XPathSelector = create_deprecated_class(
    'XPathSelector',
    Selector,
    {
        '__slots__': (),
        '_default_type': 'html',
        'css': _xpathselector_css,
    },
    new_class_path='scrapy.Selector',
    old_class_path='scrapy.selector.XPathSelector',
)

XmlXPathSelector = create_deprecated_class(
    'XmlXPathSelector',
    XPathSelector,
    clsdict={
        '__slots__': (),
        '_default_type': 'xml',
    },
    new_class_path='scrapy.Selector',
    old_class_path='scrapy.selector.XmlXPathSelector',
)

HtmlXPathSelector = create_deprecated_class(
    'HtmlXPathSelector',
    XPathSelector,
    clsdict={
        '__slots__': (),
        '_default_type': 'html',
    },
    new_class_path='scrapy.Selector',
    old_class_path='scrapy.selector.HtmlXPathSelector',
)

XPathSelectorList = create_deprecated_class('XPathSelectorList', SelectorList)
