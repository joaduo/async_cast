"""
async_cast
Copyright (c) 2021, Joaquin G. Duo

Code Licensed under MIT License. See LICENSE file.
"""
from async_cast import to_blocking, to_async, to_async_thread, thread_pool
import asyncio


async def async_func(num, msg=''):
    print(f'Calling:async_func({num} msg:{msg})')
    return num


def block_func(num, msg=''):
    print(f'Calling:block_func({num} msg:{msg})')
    return num


async def main_async():
    await async_func(3)
    await to_async(block_func)(4)
    with thread_pool(4):
        t = to_async_thread(block_func)(5)
        r = await to_async_thread(block_func)(6)
        assert r == 6
        t3 = to_async(block_func)(7)
        t4 = to_async_thread(block_func)(8, msg='8msg')
        t5 = async_func(9)
        t6 = to_async_thread(async_func)(10, msg='10msg')
        r = await asyncio.gather(t, t3, t4, t5, t6)
        assert r == [5, 7, 8, 9, 10]


def test_async_cast():
    # Run synchronic
    to_blocking(async_func)(1)
    block_func(2)
    asyncio.run(main_async())


if __name__ == '__main__':
    test_async_cast()
