#!/usr/bin/env python3
"""
 Cache class module
"""
import uuid
from typing import Union, Callable
from functools import wraps
import redis


def count_calls(method: Callable) -> Callable:
    """Count calls decorator"""

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function"""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """Call history decorator"""

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function"""
        key = method.__qualname__
        input = str(args)
        self._redis.rpush(f"{key}:inputs", input)
        output = str(method(self, *args, **kwargs))
        self._redis.rpush(f"{key}:outputs", output)
        return output

    return wrapper


def replay(method: Callable):
    """Replay decorator print history of calls of a particular function"""
    r = redis.Redis()
    key = method.__qualname__
    count = r.get(key)
    if not count:
        count = 0
    inputs = r.lrange(f"{key}:inputs", 0, -1)
    outputs = r.lrange(f"{key}:outputs", 0, -1)
    print(f"{key} was called {count} times:")
    for i, o in zip(inputs, outputs):
        print(f"{key}(*{i.decode('utf-8')}) -> {o.decode('utf-8')}")


class Cache:
    """Create a Cache class."""

    def __init__(self):
        """
        store an instance of the Redis client as a private variable
        flush the instance using
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """set a uuid for a data and cache it"""
        key: str = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(
        self, key: str, fn: Union[Callable, None] = None
    ) -> Union[str, bytes, int, float]:
        """get value and pass it to the callable"""
        value = self._redis.get(key)

        if fn is not None:
            return fn(value)

        return value

    def get_str(self, key: str) -> str:
        """parametrize method for getting a string from the cache"""
        return self.get(key, lambda x: x.decode("utf-8"))  # type: ignore

    def get_int(self, key: str) -> int:
        """parametrize method for getting an integer from the cache"""
        return self.get(key, int)  # type: ignore
