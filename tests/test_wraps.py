"""
async_cast
Copyright (c) 2021, Joaquin G. Duo

Code Licensed under MIT License. See LICENSE file.
"""
from async_cast import also_blocking, also_async, to_async, to_blocking, to_async_thread

@also_blocking
async def async_func(num):
    print(f'Calling:async_func({num})')


@also_async
def block_func(num):
    print(f'Calling:block_func({num})')


async def async_func2(num):
    print(f'Calling:async_func({num})')


def block_func2(num):
    print(f'Calling:block_func({num})')


def test_wraps():
    # Run synchronic
    assert str(async_func).startswith('<function async_func ')
    assert str(block_func).startswith('<function block_func ')
    assert str(to_async(block_func2)).startswith('<function block_func2 ')
    assert str(to_blocking(async_func2)).startswith('<function async_func2 ')
    assert str(to_async_thread(async_func2)).startswith('<function async_func2 ')


if __name__ == '__main__':
    test_wraps()
