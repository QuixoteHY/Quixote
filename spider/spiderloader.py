# -*- coding:utf-8 -*-
# @Time     : 2019-03-12 08:30
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe :

from __future__ import absolute_import
from collections import defaultdict
import traceback
import warnings
import six
import inspect

from zope.interface import implementer, Interface

from quixote.utils.misc import walk_modules


def iter_spider_classes(module):
    """Return an iterator over all spider classes defined in the given module
    that can be instantiated (ie. which have name)
    """
    # this needs to be imported here until get rid of the spider manager
    # singleton in quixote.spider.spiders
    from quixote.spider import Spider
    for obj in six.itervalues(vars(module)):
        if inspect.isclass(obj) and \
           issubclass(obj, Spider) and \
           obj.__module__ == module.__name__ and \
           getattr(obj, 'name', None):
            yield obj


class ISpiderLoader(Interface):
    def from_settings(settings):
        """Return an instance of the class for the given settings"""

    def load(spider_name):
        """Return the Spider class for the given spider name. If the spider
        name is not found, it must raise a KeyError."""

    def list():
        """Return a list with the names of all spiders available in the
        project"""

    def find_by_request(request):
        """Return the list of spiders names that can handle the given request"""


@implementer(ISpiderLoader)
class SpiderLoader(object):
    """
    SpiderLoader is a class which locates and loads spiders
    in a quixote project.
    """
    def __init__(self, settings):
        self.spider_modules = [settings['BOT_NAME']+'.'+name for name in settings['SPIDER_MODULES']]
        self.warn_only = settings['SPIDER_LOADER_WARN_ONLY']
        self._spiders = {}
        self._found = defaultdict(list)
        self._load_all_spiders()

    def get_spider_by_name(self, name):
        return self._spiders[name]

    def _check_name_duplicates(self):
        dupes = ["\n".join("  {cls} named {name!r} (in {module})".format(module=mod, cls=cls, name=name)
                           for (mod, cls) in locations) for name, locations in self._found.items()
                 if len(locations) > 1]
        if dupes:
            msg = ("There are several spiders with the same name:\n\n{}\n\n  This can cause unexpected behavior."
                   .format("\n\n".join(dupes)))
            warnings.warn(msg, UserWarning)

    def _load_spiders(self, module):
        for spcls in iter_spider_classes(module):
            self._found[spcls.name].append((module.__name__, spcls.__name__))
            self._spiders[spcls.name] = spcls

    def _load_all_spiders(self):
        for name in self.spider_modules:
            try:
                for module in walk_modules(name):
                    self._load_spiders(module)
            except ImportError as e:
                if self.warn_only:
                    msg = ("\n{tb}Could not load spiders from module '{modname}'. See above traceback for details. {e}"
                           .format(modname=name, tb=traceback.format_exc(), e=str(e)))
                    warnings.warn(msg, RuntimeWarning)
                else:
                    raise
        self._check_name_duplicates()

    @classmethod
    def from_settings(cls, settings):
        return cls(settings)

    def load(self, spider_name):
        """
        Return the Spider class for the given spider name. If the spider
        name is not found, raise a KeyError.
        """
        try:
            return self._spiders[spider_name]
        except KeyError:
            raise KeyError("Spider not found: {}".format(spider_name))

    def find_by_request(self, request):
        """
        Return the list of spider names that can handle the given request.
        """
        return [name for name, cls in self._spiders.items()
                if cls.handles_request(request)]

    def list(self):
        """
        Return a list with the names of all spiders available in the project.
        """
        return list(self._spiders.keys())
