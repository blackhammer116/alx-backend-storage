#!/usr/bin/env python3
"""
redis: to handle the cache
uuid: to generate a random id for the key value
pair
Union: for type annotation
Callable: used for type annotation
"""
import redis
import uuid
from typing import Union, Callable
from functools import wraps


def cache_calls(method: Callable) -> Callable:
    """
    creating a decorator to count calls of methods
    Args:
        method: a Callable to be counted
    """
    @wraps(method)
    def wrapped(self, *args, **kwargs):
        """
        A function that increments a callable
        by 1
        """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapped


def call_history(method: Callable) -> Callable:
    """
    A decorator to list call history of a
    method
    Args:
        method: a Callable function
    """
    @wraps(method)
    def wrapped(self, *args, **kwargs):
        """
        A wrapper function that creates a list of
        inputs and outputs to that method
        Args:
            self: to access the redis object
        """
        input_key = method.__qualname__ + ":inputs"
        output_key = method.__qualname__ + ":outputs"

        self._redis.rpush(input_key, str(args))

        output = method(self, *args, **kwargs)

        self._redis.rpush(output_key, str(output))
        return output
    return wrapped


class Cache():
    """
    Cache class to start handling the cache using redis
    """
    def __init__(self):
        """
        Init method to define the private attribute _redis
        and flushing the instance
        """
        self._redis = redis.Redis()

        self._redis.flushdb()

    @cache_calls
    @call_history
    def store(self, data: Union[str, int, float, bytes]) -> str:
        """
        A method that sets a random uuid key to the value(data)
        and returns a key
        Args:
            data: the value to be set on the key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)

        return key

    def get(self, key: str, fn: Callable = None) -> \
            Union[int, str, float, bytes, None]:
        """
        A method that gets the value of the redis using the key
        and returning the value with the desired type
        Args:
            key: key of the redis
            fn: A Callable function
        """
        value = self._redis.get(key)
        if fn is None:
            return value
        if value is None:
            return None
        return fn(value)

    def get_str(self, key: str) -> Union[str, None]:
        """
        A method that automatically return the value of get method
        to the desired type in our case str
        Args:
            key: key of the redis
        """
        return self.get(key, str)

    def get_int(self, key: str) -> Union[int, None]:
        """
        A method that automatically return the value
        by the desired type in this case INT
        Args:
            key: key of the redis
        """
        return self.get(key, int)


def replay(func: Callable):
    input_key = func.__qualname__ + ":inputs"
    output_key = func.__qualname__ + ":outputs"

    cache = func.__self__

    inputs = cache._redis.lrange(input_key, 0, -1)
    outputs = cache._redis.lrange(output_key, 0, -1)

    print(f"{func.__qualname__} was called {len(inputs)} times:")

    for inp, out in zip(inputs, outputs):
        input_args = eval(inp.decode())
        output_value = out.decode()
        print(f"{func.__qualname__}(*{input_args}) -> {output_value}")
