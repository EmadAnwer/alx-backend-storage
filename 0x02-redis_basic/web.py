#!/usr/bin/env python3
""" Redis Module """

from functools import wraps
from typing import Union, Callable
import redis
import uuid


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


