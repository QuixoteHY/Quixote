
# Mac: brew install telnet

import asyncio
import telnetlib3


@asyncio.coroutine
def shell(reader, writer):
    writer.write('\r\nWould you like to play a game? ')
    inp = yield from reader.read(1)
    if inp:
        writer.echo(inp)
        writer.write('\r\nThey say the only way to win '
                     'is to not play at all.\r\n')
        yield from writer.drain()
    writer.close()


@asyncio.coroutine
def shell2(reader, writer):
    while True:
        writer.write('\r\n>')
        inp = yield from reader.read(1)
        if inp:
            print(type(inp), '\t', inp)
            writer.echo(inp)
            writer.write('\r\nThey say the only way to win '
                         'is to not play at all.\r\n')
            yield from writer.drain()
        if inp == 'exit':
            break
        if inp == '\r':
            print('\\r')
        if inp == '\n':
            print('\\n')
    writer.close()


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
def shell3(reader, writer):
    writer.write('\r\n>Quixote Telnet')
    yield from writer.drain()
    while True:
        try:
            writer.write('\r\n>')
            word = yield from read_word(reader, writer)
            if word == 'exit':
                break
            writer.write('\r\n'+word)
            yield from writer.drain()
        except Exception as e:
            print(e)
    writer.close()


loop = asyncio.get_event_loop()
# coro = telnetlib3.create_server(port=6023, shell=shell)
# coro = telnetlib3.create_server(port=6023, shell=shell2)
coro = telnetlib3.create_server(port=6023, shell=shell3)
server = loop.run_until_complete(coro)
loop.run_until_complete(server.wait_closed())
