
import asyncio


async def aa():
    await asyncio.sleep(0.1)
    return 'http://www.baidu.com'


def callback(future):
    print('response.url: '+future.result())
    # future = asyncio.Future()
    # future.set_result('http://www.youtube.com')
    # future._state = 'PENDING'
    # setattr(future, '_state', 'PENDING')
    print(type(future))
    print(future._state)
    print(future.__asyncioTask__result)
    future._Task___state = 'PENDING'
    # future.set_result('http://www.youtube.com')


task = asyncio.ensure_future(aa())
task.add_done_callback(callback)


loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(*[task]))

print('return: '+task.result())

loop.close()






