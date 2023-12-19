"""
async_cast
Copyright (c) 2021, Joaquin G. Duo

Code Licensed under MIT License. See LICENSE file.
"""
from async_cast import async_thread, thread_pool
import asyncio


@async_thread
async def async_func(num, msg=''):
    print(f'Calling:async_func({num} msg:{msg})')
    return num


@async_thread
def block_func(num, msg=''):
    print(f'Calling:block_func({num} msg:{msg})')
    return num


async def main_async():
    with thread_pool(4):
        t = block_func.async_thread(5)
        r = await block_func.async_thread(6)
        assert r == 6
        t4 = block_func.async_thread(8, msg='8msg')
        t6 = async_func.async_thread(10, msg='10msg')
        r = await asyncio.gather(t, t4, t6)
        assert r == [5, 8, 10]


def test_async_cast():
    asyncio.run(main_async())


if __name__ == '__main__':
    test_async_cast()
