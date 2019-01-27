import asyncio

bk = None
print(id(bk))


async def task(text):
    print(text)
    return text


def c1(future):
    text = future.result()+' In c1...'
    print(text)
    bk = text
    print(id(bk))
    return text


async def run():
    t = asyncio.ensure_future(task('In task...'))
    t.add_done_callback(c1)
    done, pending = await asyncio.wait({t})
    response = None
    if t in done:
        response = t.result()
    return response


async def run2():
    aaaa = None

    def z1(future):
        text = future.result() + ' In c1...'
        print(text)
        aaaa = text
        return text
    t = asyncio.ensure_future(task('In task...'))
    t.add_done_callback(z1)
    done, pending = await asyncio.wait({t})
    response = None
    if t in done:
        response = t.result()

    print('aaaa: '+str(aaaa))
    return response


loop = asyncio.get_event_loop()
loop.run_until_complete(run2())
loop.close()




