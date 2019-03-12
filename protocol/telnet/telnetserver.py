# -*- coding:utf-8 -*-
# @Time     : 2019-02-28 13:02
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe :

import asyncio

import telnetlib3


class TelnetServer(object):
    def __init__(self):
        self.engine = None
        self.telnet_vars = None

    @staticmethod
    @asyncio.coroutine
    def read_word(reader, writer):
        word = ''
        while True:
            inp = yield from reader.read(1)
            writer.echo(inp)
            if inp == '\r':
                return word
            word += inp

    @asyncio.coroutine
    def shell(self, reader, writer):
        total_concurrency = self.engine.downloader.total_concurrency
        self.engine.downloader.total_concurrency = 10
        writer.write('\r\nWelcome to Quixote Telnet!\r\nYou need to be patient and wait for the start...\r\n...')
        yield from writer.drain()
        while True:
            try:
                writer.write('\r\n>>>')
                word = yield from self.read_word(reader, writer)
                if word == 'exit':
                    break
                response = self.get_response(word)
                writer.write('\r\n'+response)
                yield from writer.drain()
            except Exception as e:
                print(e)
        writer.close()
        self.engine.downloader.total_concurrency = total_concurrency

    def get_response(self, variable_name):
        if variable_name in self.telnet_vars:
            res = self.telnet_vars[variable_name]()
            return res
        return 'ERROR COMMAND'

    def create_server(self, port, engine, telnet_vars):
        self.engine = engine
        self.telnet_vars = telnet_vars
        return telnetlib3.create_server(port=port, shell=self.shell)
