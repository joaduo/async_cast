"""
asyncio_threads
Copyright (c) 2021, Joaquin G. Duo

Code Licensed under MIT License. See LICENSE file.
"""
import asyncio
import concurrent.futures
import inspect


def thread_pool(max_workers=None, *args, **kwargs):
    """
    Create a ThreadPoolExecutor pool to run functions decorated with `@also_async` and `@also_sync`

    Accepts same arguments as `concurrent.futures.ThreadPoolExecutor`
    Args:
        max_workers: The maximum number of threads that can be used to
            execute the given calls.
        thread_name_prefix: An optional name prefix to give our threads.
        initializer: A callable used to initialize worker threads.
        initargs: A tuple of arguments to pass to the initializer.
    """
    return _DecoratorBase.thread_pool(max_workers, *args, **kwargs)


class _DecoratorBase:
    """
    Allows using `ThreadPoolExecutor` when calling `async_thread(...)`
    Avoids having to pass the executor to submit the async job to the ThreadPoolExecutor
    """
    _pools_stack = []
    @classmethod
    def _push_pool(cls, pool): 
        cls._pools_stack.append(pool)

    @classmethod
    def _pop_pool(cls):
        return cls._pools_stack.pop()

    @classmethod
    def _get_pool(cls):
        assert cls._pools_stack, ('Run this task in a pool context using '
                                 f'"with {cls.__name__}.thread_pool():..."')
        return cls._pools_stack[-1]

    @classmethod
    def thread_pool(cls, max_workers=None, *args, **kwargs):
        pool = concurrent.futures.ThreadPoolExecutor(max_workers, *args, **kwargs)
        cls._push_pool(pool)
        class PoolContext:
            def __enter__(self):
                return pool.__enter__()
            def __exit__(self, exc_type, exc_val, exc_tb):
                cls._pop_pool()
                return pool.__exit__(exc_type, exc_val, exc_tb)
        return PoolContext()

    def __init__(self, wrapped_func):
        self._wrapped_func = wrapped_func

    def __call__(self, *args, **kwargs):
        return self._wrapped_func(*args, **kwargs)

    def async_thread(self, *args, **kwargs):
        fn = self._wrapped_func
        if inspect.iscoroutinefunction(fn):
            fn = self.sync
        loop = asyncio.get_running_loop()
        # run_in_executor only allows *args (positional), so we use self._run_fn
        return loop.run_in_executor(self._get_pool(),
                                    self._run_fn, fn, args, kwargs)

    def _run_fn(self, fn, args, kwargs):
        return fn(*args, **kwargs)


class also_async(_DecoratorBase):
    """
    Cast sync function to async
    """
    def sync(self, *args, **kwargs):
        return self._wrapped_func(*args, **kwargs)

    async def async_(self, *args, **kwargs):
        return self._wrapped_func(*args, **kwargs)


class also_sync(_DecoratorBase):
    """
    Cast async function to sync
    """
    def sync(self, *args, **kwargs):
        return asyncio.run(self(*args, **kwargs))

    def async_(self, *args, **kwargs):
        return self(*args, **kwargs)



