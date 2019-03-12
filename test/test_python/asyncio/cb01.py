
import asyncio
from quixote.protocol.response import Response


async def aa():
    await asyncio.sleep(0.1)
    return Response('http://www.baidu.com', )


def callback(future):
    print('response.url: '+future.result().url)
    future.result().url = 'http://www.youtube.com'


task = asyncio.ensure_future(aa())
task.add_done_callback(callback)


loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(*[task]))

print('return: '+task.result().url)

loop.close()






