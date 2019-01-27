import asyncio


async def task(text):
    # await asyncio.sleep(1)
    print(text)
    return text


async def task1(text):
    # await asyncio.sleep(1)
    print(text)
    return text


async def task11(text):
    a = await task1(text)
    print(text)
    return text


def c1(future):
    text = future.result()+' In c1...'
    print(text)
    return text


def c2(future):
    text = future.result()+' In c2...'
    print(text)
    return text


task = asyncio.ensure_future(task('In task...'))
task.add_done_callback(c1)
task.add_done_callback(c2)

task1 = asyncio.ensure_future(task1('In task1...'))
task1.add_done_callback(c1)
task1.add_done_callback(c2)


loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(*[task, task1]))
loop.close()

