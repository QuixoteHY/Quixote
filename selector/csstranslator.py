# -*- coding:utf-8 -*-
# @Time     : 2019-01-19 00:38
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe : XPath selectors based on lxml

from parsel.csstranslator import XPathExpr, GenericTranslator, HTMLTranslator

from quixote.utils.deprecate import create_deprecated_class


ScrapyXPathExpr = create_deprecated_class('ScrapyXPathExpr', XPathExpr, new_class_path='parsel.csstranslator.XPathExpr')

ScrapyGenericTranslator = create_deprecated_class('ScrapyGenericTranslator', GenericTranslator,
                                                  new_class_path='parsel.csstranslator.GenericTranslator')

ScrapyHTMLTranslator = create_deprecated_class('ScrapyHTMLTranslator', HTMLTranslator,
                                               new_class_path='parsel.csstranslator.HTMLTranslator')
