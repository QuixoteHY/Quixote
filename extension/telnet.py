# -*- coding:utf-8 -*-
# @Time     : 2019-02-28 08:42
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe :

try:
    import telnetlib3
    TWISTED_CONCH_AVAILABLE = True
except ImportError:
    TWISTED_CONCH_AVAILABLE = False

from quixote.signals import engine_started, engine_stopped
from quixote.logger import logger
from quixote.exceptions import NotConfigured


class TelnetConsole(object):
    def __init__(self, starter):
        if not starter.settings['TELNETCONSOLE_ENABLED']:
            raise NotConfigured
        if not TWISTED_CONCH_AVAILABLE:
            raise NotConfigured
        self.starter = starter
        self.noisy = False
        self.portrange = [int(x) for x in starter.settings['TELNETCONSOLE_PORT']]
        self.host = starter.settings['TELNETCONSOLE_HOST']
        self.starter.signals.connect(self.start_listening, engine_started)
        self.starter.signals.connect(self.stop_listening, engine_stopped)

    @classmethod
    def from_starter(cls, starter):
        return cls(starter)

    def start_listening(self):
        logger.info("Telnet console listening on %(host)s:%(port)d", {'host': self.host, 'port': self.portrange[0]},
                    extra={'starter': self.starter})

    def stop_listening(self):
        pass
