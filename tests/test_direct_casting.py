"""
async_cast
Copyright (c) 2021, Joaquin G. Duo

Code Licensed under MIT License. See LICENSE file.
"""
from async_cast import to_blocking, to_async, to_async_thread, thread_pool
import asyncio


async def async_func(num):
    print(f'Calling:async_func({num})')


def block_func(num):
    print(f'Calling:block_func({num})')


async def main_async():
    await async_func(2)
    await to_async(block_func, 2)
    with thread_pool(4):
        t = to_async_thread(block_func, 3)
        await to_async_thread(block_func, 4)
        t3 = to_async(block_func, 5)
        t4 = to_async_thread(block_func, 6)
        t5 = async_func(3)
        t6 = to_async_thread(async_func, 4)
        await asyncio.gather(t, t3, t4, t5, t6)


def test_async_cast():
    # Run synchronic
    to_blocking(async_func, 1)
    block_func(1)
    asyncio.run(main_async())


if __name__ == '__main__':
    test_async_cast()
