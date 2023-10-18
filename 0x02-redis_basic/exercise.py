#!/usr/bin/env python3
"""
redis: to handle the cache
uuid: to generate a random id for the key value
pair
Union: for type annotation
"""
import redis
import uuid
from typing import Union


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

    def store(self, data: Union[str, int, float, bytes]) -> str:
        """
        A method that sets a random uuid key to the value(data) and returns a key
        Args:
            data: the value to be set on the key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        
        return key

