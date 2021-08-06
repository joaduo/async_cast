"""
async_cast
Copyright (c) 2021, Joaquin G. Duo

Code Licensed under MIT License. See LICENSE file.
"""
from async_cast import also_blocking, also_async, thread_pool
import asyncio


@also_blocking
async def async_func(num):
    print(f'Calling:async_func({num})')


@also_async
def block_func(num):
    print(f'Calling:block_func({num})')


async def main_async():
    await async_func(2)
    await block_func.async_(2)
    with thread_pool(4):
        t = block_func.async_thread(3)
        await block_func.async_thread(4)
        t3 = block_func.async_(5)
        t4 = block_func.async_thread(6)
        t5 = async_func(3)
        t6 = async_func.async_thread(4)
        await asyncio.gather(t, t3, t4, t5, t6)


def test_async_cast():
    # Run synchronic
    async_func.blocking(1)
    block_func(1)
    asyncio.run(main_async())


if __name__ == '__main__':
    test_async_cast()
