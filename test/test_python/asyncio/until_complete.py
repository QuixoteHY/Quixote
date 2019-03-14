
import time
import asyncio


async def aa():
    await asyncio.sleep(9)
    print('aa')


async def bb():
    await asyncio.sleep(3)
    print('bb')


loop = asyncio.get_event_loop()

loop.run_until_complete(aa())

print('*'*8)
time.sleep(2)
print('-'*8)

loop.run_until_complete(bb())


