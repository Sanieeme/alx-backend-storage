#!/usr/bin/env python3
""" """
import uuid
import redis
from typing import Union


class Cache:
    """class"""
    def __init__(self):
        """
        initialization store an instance of the Redis client
        as a private variable
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        takes a data argument and returns a string
        Args:
            data: can either be str, bytes, int or float
        Returns:
            str
        """
        if isinstance(data, (str, bytes, int, float)):
            key = str(uuid.uuid4())
            self._redis.set(key, data)
            return key
