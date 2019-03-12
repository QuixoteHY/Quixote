
import time
import asyncio
import aiohttp


async def aaa():
    await asyncio.sleep(100)

#
loop = asyncio.get_event_loop()

asyncio.run_coroutine_threadsafe(aaa(), loop)
#
#
# while True:
#     time.sleep(3)
#     asyncio.run_coroutine_threadsafe(aaa(), loop)


session = aiohttp.ClientSession()

# session.close()

# UserWarning: Creating a client session outside of coroutine is a very dangerous idea
# asyncio.run_coroutine_threadsafe(session.close(), loop)

loop.run_until_complete(session.close())
loop.close()


