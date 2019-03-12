# -*- coding:utf-8 -*-
# @Time     : 2019-02-28 08:42
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe :

from __future__ import print_function
import time
import asyncio

try:
    import telnetlib3
    TELNET_LIB_AVAILABLE = True
except ImportError:
    TELNET_LIB_AVAILABLE = False

from quixote.signals import engine_started, engine_stopped
from quixote import loop
from quixote.logger import logger
from quixote.protocol import TelnetServer
from quixote.exceptions import NotConfigured


class StateInspector(object):
    def __init__(self, starter):
        self.starter = starter

    def get_engine_status(self):
        """Return a report of the current engine status"""
        engine = self.starter.engine
        tests = [
            "time.time()-engine.start_time",
            # "engine.has_capacity()",
            "len(engine.downloader.active)",
            # "engine.scraper.is_idle()",
            "engine.spider.name",
            # "engine.spider_is_idle(engine.spider)",
            # "engine.slot.closing",
            # "len(engine.slot.inprogress)",
            # "len(engine.slot.scheduler.dqs or [])",
            # "len(engine.slot.scheduler.mqs)",
            "len(engine.scraper.slot.queue)",
            "len(engine.scraper.slot.active)",
            "engine.scraper.slot.active_size",
            "engine.scraper.slot.itemproc_size",
            "engine.scraper.slot.needs_slowdown()",
        ]
        checks = []
        for test in tests:
            try:
                checks += [(test, eval(test))]
            except Exception as e:
                checks += [(test, "%s (exception)" % type(e).__name__)]
        return checks

    def format_engine_status(self):
        checks = self.get_engine_status()
        s = "-"*80+"\r\n"+"Quixote engine status\r\n"+"-"*80+"\r\n"
        for test, result in checks:
            s += "%-47s : %s\r\n" % (test, result)
        return s

    @staticmethod
    def help():
        return 'This is Quixote telnet console. '

    def print_engine_status(self):
        print(self.format_engine_status())


class TelnetConsole(object):
    def __init__(self, starter):
        if not starter.settings['TELNETCONSOLE_ENABLED']:
            raise NotConfigured
        if not TELNET_LIB_AVAILABLE:
            raise NotConfigured
        self.starter = starter
        self.noisy = False
        self.portrange = [int(x) for x in starter.settings['TELNETCONSOLE_PORT']]
        self.host = starter.settings['TELNETCONSOLE_HOST']
        self.starter.signals.connect(self.start, engine_started)
        self.starter.signals.connect(self.stop, engine_stopped)
        self.telnet_server = TelnetServer()
        self.engine = None
        self.state_inspector = StateInspector(self.starter)
        self.telnet_vars = {
            # 'engine': self.starter.engine,
            # 'spider': self.starter.engine.spider,
            # 'slot': self.starter.engine.slot,
            # 'crawler': self.starter,
            # 'extensions': self.starter.extensions,
            # 'stats': self.starter.stats,
            # 'settings': self.starter.settings,
            'est': self.state_inspector.format_engine_status,
            # 'p': pprint.pprint,
            # 'prefs': print_live_refs,
            # 'hpy': hpy,
            'help': self.state_inspector.help,
        }

    @classmethod
    def from_starter(cls, starter):
        return cls(starter)

    def start(self, sender):
        self.engine = sender
        logger.info("Telnet console listening on %(host)s:%(port)d", {'host': self.host, 'port': self.portrange[0]},
                    extra={'starter': self.starter})
        logger.info(type(self.engine))
        asyncio.run_coroutine_threadsafe(
            self.telnet_server.create_server(self.portrange[0], self.engine, self.telnet_vars), loop)

    def stop(self, sender):
        pass
