"""
async_cast
Copyright (c) 2021, Joaquin G. Duo

Code Licensed under MIT License. See LICENSE file.
"""
from async_cast import also_sync, also_async, thread_pool
import asyncio


@also_sync
async def async_func(num):
    print(f'Calling:async_func({num})')


@also_async
def sync_func(num):
    print(f'Calling:sync_func({num})')


async def main_async():
    await async_func(2)
    await sync_func.async_(2)  
    with thread_pool(2):
        t = sync_func.async_thread(3)
        await sync_func.async_thread(4)
        t3 = sync_func.async_(5)
        t4 = sync_func.async_thread(6)
        t5 = async_func(3)
        t6 = async_func.async_thread(4)
        await asyncio.gather(t, t3, t4, t5, t6)


def test():
    # Run synchronic
    async_func.sync(1)
    sync_func(1)
    asyncio.run(main_async())


if __name__ == '__main__':
    test()
