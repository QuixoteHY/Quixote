
import asyncio
from quixote import Response


async def aa():
    await asyncio.sleep(0.1)
    return 'http://www.baidu.com'


def callback(future):
    print('response.url: '+future.result())
    # future.result().url = future.result().url+'*'*10


async def run():
    task = asyncio.ensure_future(aa())
    task.add_done_callback(callback)

    done, pending = await asyncio.wait({task})
    response = None
    if task in done:
        response = task.result()
    print(response)


loop = asyncio.get_event_loop()
loop.run_until_complete(run())
loop.close()






