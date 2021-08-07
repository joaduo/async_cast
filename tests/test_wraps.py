"""
async_cast
Copyright (c) 2021, Joaquin G. Duo

Code Licensed under MIT License. See LICENSE file.
"""
from async_cast import also_blocking, also_async

@also_blocking
async def async_func(num):
    print(f'Calling:async_func({num})')


@also_async
def block_func(num):
    print(f'Calling:block_func({num})')


def test_wraps():
    # Run synchronic
    assert str(async_func).startswith('<function async_func')
    assert str(block_func).startswith('<function block_func')


if __name__ == '__main__':
    test_wraps()
