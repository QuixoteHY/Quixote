# -*- coding:utf-8 -*-
# @Time     : 2019-02-27 19:47
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe :

from pydispatch import dispatcher


class SignalManager(object):
    def __init__(self):
        self.sender = dispatcher.Any

    def connect(self, receiver, signal):
        return dispatcher.connect(receiver, signal, self.sender)

    def send(self, signal, sender):
        dispatcher.send(signal=signal, sender=sender)

    def disconnect(self, receiver, signal):
        return dispatcher.disconnect(receiver, signal)
