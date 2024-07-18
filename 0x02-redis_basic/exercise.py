#!/usr/bin/env python3
""" """
import uuid
import redis
from typing import Callable, Optional, Any, Union, Dict, List
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """ """
    @wraps(method)
    def wrapper(self, *args, **kwds):
        """Wrapper function to count method calls."""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwds)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator to track method call history using Redis.

    Args:
        method (Callable): Method to decorate.

    Returns:
        Callable: Decorated method with history tracking.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__

        # Store inputs
        inputs_key = f"{key}:inputs"
        self._redis.rpush(inputs_key, str(args))

        # Call the original method
        result = method(self, *args, **kwargs)

        # Store output
        outputs_key = f"{key}:outputs"
        self._redis.rpush(outputs_key, str(result))

        return result

    return wrapper


class Cache:
    """class"""
    def __init__(self):
        """
        initialization store an instance of the Redis client
        as a private variable
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @staticmethod
    def replay(method: Callable) -> None:
        """
        Replay the method calls recorded in Redis.

        Args:
            method (Callable): The method to replay the calls for.
        """
        cache_instance = method.__self__  # Get the instance of the cache
        key = method.__qualname__
        inputs_key = f"{key}:inputs"
        outputs_key = f"{key}:outputs"

        # Fetch inputs and outputs from Redis
        inputs = cache_instance._redis.lrange(inputs_key, 0, -1)
        outputs = cache_instance._redis.lrange(outputs_key, 0, -1)

        # Format and print the replay output
        num_calls = len(inputs)
        print(f"{key} was called {num_calls} times:")

        for input_data, output_data in zip(inputs, outputs):
            input_str = input_data.decode('utf-8')
            output_str = output_data.decode('utf-8')
            print(f"{key}(*{input_str}) -> {output_str}")

    @count_calls
    @call_history
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

    @count_calls
    @call_history
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

    def get_call_count(self, method_name: str) -> int:
        """
        Get the call count for a specific method.

        Args:
            method_name: The qualified name of the method

        Returns:
            in.
        """
        return int(self._redis.get(method_name) or 0)
