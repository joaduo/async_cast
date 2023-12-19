"""
async_cast
Copyright (c) 2021, Joaquin G. Duo

Code Licensed under MIT License. See LICENSE file.
"""
import asyncio
import concurrent.futures
import inspect
from functools import wraps


def thread_pool(max_workers=None, *args, **kwargs):
    """
    Create a ThreadPoolExecutor pool to run functions decorated with `@also_async` and `@also_blocking`

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

    def __init__(self, wrapped):
        self._wrapped = wrapped

    def __call__(self, *args, **kwargs):
        return self._wrapped(*args, **kwargs)

    def async_thread(self, *args, **kwargs):
        fn = self._wrapped
        if inspect.iscoroutinefunction(fn):
            fn = self._blocking
        loop = asyncio.get_running_loop()
        # run_in_executor only allows *args (positional), so we use self._run_fn
        return loop.run_in_executor(self._get_pool(),
                                    self._run_fn, fn, args, kwargs)

    def _run_fn(self, fn, args, kwargs):
        return fn(*args, **kwargs)

    def _blocking(self, *args, **kwargs):
        return asyncio.run(self(*args, **kwargs))


WRAPPER_ASSIGNMENTS = ('blocking', 'async_', 'async_thread')


def also_async(func):
    """
    Decorator allowing casting blocking function to async function
    """
    return __also_async(func)


def __also_async(func, assignments=WRAPPER_ASSIGNMENTS):
    assert not inspect.iscoroutinefunction(func) and callable(func), 'You need to decorate a blocking function'
    @wraps(func)
    def wrapper(*a, **kw):
        return func(*a, **kw)
    instance = _also_async(func)
    for attr in WRAPPER_ASSIGNMENTS:
        setattr(wrapper, attr, getattr(instance, attr))
    return wrapper


class _also_async(_DecoratorBase):
    def blocking(self, *args, **kwargs):
        return self._wrapped(*args, **kwargs)

    async def async_(self, *args, **kwargs):
        return self._wrapped(*args, **kwargs)


def also_blocking(func):
    """
    Decorator allowing casting async function to blocking function
    """
    return __also_blocking(func)


def __also_blocking(func, assignments=WRAPPER_ASSIGNMENTS):
    assert inspect.iscoroutinefunction(func), 'You need to decorate a coroutine'
    @wraps(func)
    def wrapper(*a, **kw):
        return func(*a, **kw)
    instance = _also_blocking(func)
    for attr in assignments:
        setattr(wrapper, attr, getattr(instance, attr))
    return wrapper


class _also_blocking(_DecoratorBase):
    def blocking(self, *args, **kwargs):
        return self._blocking(*args, **kwargs)

    def async_(self, *args, **kwargs):
        return self(*args, **kwargs)


def async_thread(func):
    """
    Decorator adding the `<func>.async_thread` attribute
    """
    assignments = ('async_thread',)
    if inspect.iscoroutinefunction(func):
        wrapper = also_blocking(func, assignments)
    else:
        wrapper = also_async(func, assignments)
    return wrapper


def to_async(func):
    """
    Cast blocking function to async function
    :param func:
    """
    assert not inspect.iscoroutinefunction(func) and callable(func), 'You need to cast a blocking function'
    casted_func = _also_async(func)
    @wraps(func)
    def wrapper(*a, **kw):
        return casted_func.async_(*a, **kw)
    return wrapper


def to_blocking(func):
    """
    Cast async function to blocking function
    :param func:
    """
    assert inspect.iscoroutinefunction(func), 'You need to cast a coroutine'
    casted_func = _also_blocking(func)
    @wraps(func)
    def wrapper(*a, **kw):
        return casted_func.blocking(*a, **kw)
    return wrapper


def to_async_thread(func):
    """
    Cast any function (async or blocking) to async_thread
    To be used with `with thread_pool(...):`
    :param func:
    """
    assert callable(func), 'You need to cast a function'
    casted_func = _DecoratorBase(func)
    @wraps(func)
    def wrapper(*a, **kw):
        return casted_func.async_thread(*a, **kw)
    return wrapper

