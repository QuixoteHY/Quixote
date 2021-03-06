# -*- coding:utf-8 -*-
# @Time     : 2019-02-26 08:56
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe : Quixote core exceptions
"""
These exceptions are documented in docs/topics/exceptions.rst. Please don't add
new exceptions here without documenting them there.
"""

# Internal


class NotConfigured(Exception):
    """Indicates a missing configuration situation"""
    pass

# HTTP and crawling


class IgnoreRequest(Exception):
    """Indicates a decision was made not to process a request"""


class DontCloseSpider(Exception):
    """Request the spider not to be closed yet"""
    pass


class CloseSpider(Exception):
    """Raise this from callbacks to request the spider to be closed"""

    def __init__(self, reason='cancelled'):
        super(CloseSpider, self).__init__()
        self.reason = reason

# Items


class DropItem(Exception):
    """Drop item from the item pipeline"""
    pass


class NotSupported(Exception):
    """Indicates a feature or method is not supported"""
    pass

# Commands


class UsageError(Exception):
    """To indicate a command-line usage error"""
    def __init__(self, *a, **kw):
        self.print_help = kw.pop('print_help', True)
        super(UsageError, self).__init__(*a, **kw)


class QuixoteDeprecationWarning(Warning):
    """Warning category for deprecated features, since the default
    DeprecationWarning is silenced on Python 2.7+
    """
    pass


class ContractFail(AssertionError):
    """Error raised in case of a failing contract"""
    pass

# Other


class NoCallbackError(Exception):
    pass


class NoRequestInQueue(Exception):
    pass


class NotSupportedURLScheme(Exception):
    pass


class ErrorNeedExit(Exception):
    pass


class ErrorSettings(ErrorNeedExit):
    pass
