# async_cast
Cast async function sync (blocking) and viceversa. Also run in threads sync and async functions.


## Casting `async` function to a sync/blocking function

```python
from async_cast import also_sync

@also_sync
async def request_url(url, **kwargs):
    print(f'Requestion {url} with options {kwargs}')
    ...
    result = f'<h1>{url}</h1>'
    return result

if __name__ == '__main__':
    print(request_url.sync('https://github.com'))
```

## Casting a sync/blocking function to `async` function

from async_cast import also_sync, also_async, thread_pool

```python
from async_cast import also_async
import asyncio

@also_async
def request_url(url, **kwargs):
    print(f'Requestion {url} with options {kwargs}')
    ...
    result = f'<h1>{url}</h1>'
    return result

async def main():
    print(await request_url.async_('https://github.com'))

if __name__ == '__main__':
    asyncio.run(main())
```

## Running `async` function in threadpool

```python
from async_cast import also_sync, thread_pool
import asyncio

@also_sync
async def request_url(url, **kwargs):
    print(f'Requestion {url} with options {kwargs}')
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

## Running sync/blocking function in threadpool

```python
from async_cast import also_async, thread_pool
import asyncio

@also_async
def request_url(url, **kwargs):
    print(f'Requestion {url} with options {kwargs}')
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

