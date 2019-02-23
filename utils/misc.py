# -*- coding:utf-8 -*-
# @Time     : 2018-12-31 19:42
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe :

from importlib import import_module
import six


def load_object(path):
    try:
        dot = path.rindex('.')
    except ValueError:
        raise ValueError("Error loading object '%s': not a full path" % path)
    module, name = path[:dot], path[dot+1:]
    mod = import_module(module)
    try:
        obj = getattr(mod, name)
    except AttributeError:
        raise NameError("Module '%s' doesn't define any object named '%s'" % (module, name))

    return obj


def fun_name(f):
    return '%s.%s' % (six.get_method_self(f).__class__.__name__, six.get_method_function(f).__name__)


def is_iterable(possible_iterator):
    return hasattr(possible_iterator, '__iter__')
