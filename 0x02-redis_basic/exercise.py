#!/usr/bin/env python3
""" """
import uuid
import redis
from typing import Callable, Optional, Any, Union


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

    def get(self, key: str, fn: Optional[Callable[[bytes], Any]] = None) -> Any:
        """
        Retrieve data from Redis
        Args:
            key: The key for the data to retrieve.
            fn: An optional callable that takes a byte strin

        Returns:
            The retrieved data, optionally transformed by fn, or None
        """
        value = self._redis.get(key)
        if value is None:
            return None
        if fn:
            return fn(value)
        return value

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve a string value from Redis.

        Args:
            key: The key for the data to retrieve.

        Returns:
            str: The retrieved data as a string, or None
        """
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve an integer value from Redis.

        Args:
            key: The key for the data to retrieve.

        Returns:
            int: The retrieved data as an int
        """
        return self.get(key, lambda x: int(x.decode('utf-8')))
