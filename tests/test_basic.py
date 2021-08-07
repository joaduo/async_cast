"""
async_cast
Copyright (c) 2021, Joaquin G. Duo

Code Licensed under MIT License. See LICENSE file.
"""
from async_cast import also_blocking, also_async, thread_pool
import asyncio


@also_blocking
async def async_func(num, msg=''):
    print(f'Calling:async_func({num} msg:{msg})')
    return num


@also_async
def block_func(num, msg=''):
    print(f'Calling:block_func({num} msg:{msg})')
    return num


async def main_async():
    await async_func(3)
    await block_func.async_(4)
    with thread_pool(4):
        t = block_func.async_thread(5)
        r = await block_func.async_thread(6)
        assert r == 6
        t3 = block_func.async_(7)
        t4 = block_func.async_thread(8, msg='8msg')
        t5 = async_func(9)
        t6 = async_func.async_thread(10, msg='10msg')
        r = await asyncio.gather(t, t3, t4, t5, t6)
        assert r == [5, 7, 8, 9, 10]


def test_async_cast():
    # Run synchronic
    async_func.blocking(1)
    block_func(2)
    asyncio.run(main_async())


if __name__ == '__main__':
    test_async_cast()
