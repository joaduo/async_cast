# async_cast

[![Codeship Status for joaduo/async_cast](https://app.codeship.com/projects/30c11a6e-2132-4298-8dbb-2b01e8cf3bac/status?branch=main)](https://app.codeship.com/projects/450075)

Cast async function to blocking and viceversa. (works on python 3.7 and up)
Also run functions in threads, whether async or blocking.

## Why `async_cast`?

I found the current `asyncio` tools frustrating when migrating from blocking code.
If you want to profit IO operations to *"run something else"* you need to rewrite all code to use
asyncio. When you start form scratch that's acceptable, but not with legacy code.

So with this small self-contained library you can easily convert legacy code into async code.
The best way is running several blocking function in different threads. But **be aware** that threads
also bring race conditions, so make sure concurrent functions are thread-safe.

## Installing

https://pypi.org/project/async-cast/

```
pip install -U async-cast
```

The package is a single module that you can easily audit. 

## Casting `async` function to a blocking function

```python
from async_cast import also_blocking

@also_blocking
async def request_url(url, **kwargs):
    print(f'Requesting {url} with options {kwargs}')
    ...
    result = f'<h1>{url}</h1>'
    return result

if __name__ == '__main__':
    print(request_url.blocking('https://github.com'))
```

## Casting a blocking function to `async` function

```python
from async_cast import also_async
import asyncio

@also_async
def request_url(url, **kwargs):
    print(f'Requesting {url} with options {kwargs}')
    ...
    result = f'<h1>{url}</h1>'
    return result

async def main():
    print(await request_url.async_('https://github.com'))

if __name__ == '__main__':
    asyncio.run(main())
```

## Running tasks in a ThreadPool

I wrapped existing `ThreadPoolExecutor` to make it easier to run tasks inside it.
Tasks are automatically registered in the pool declared by the `with thread_pool(...):` context.

### Running `async` function in threadpool

```python
from async_cast import also_blocking, thread_pool
import asyncio

@also_blocking
async def request_url(url, **kwargs):
    print(f''Requesting {url} with options {kwargs}')
    ...
    result = f'<h1>{url}</h1>'
    return result

async def main():
    with thread_pool(3):
        t1 = request_url.async_thread('https://github.com')
        t2 = request_url.async_thread('https://google.com')
        t3 = request_url.async_thread('https://facebook.com')
        results = await asyncio.gather(t1,t2,t3)
        print(results)

if __name__ == '__main__':
    asyncio.run(main())
```

### Running blocking function in threadpool

```python
from async_cast import also_async, thread_pool
import asyncio

@also_async
def request_url(url, **kwargs):
    print(f'Requesting {url} with options {kwargs}')
    ...
    result = f'<h1>{url}</h1>'
    return result

async def main():
    with thread_pool(3):
        t1 = request_url.async_thread('https://github.com')
        t2 = request_url.async_thread('https://google.com')
        t3 = request_url.async_thread('https://facebook.com')
        results = await asyncio.gather(t1,t2,t3)
        print(results)

if __name__ == '__main__':
    asyncio.run(main())
```

