import collections
import contextlib
import functools
import time
from typing import Callable


class Debouncer:
    """
    Wrap a function to limit its execution count within a given time span.
    Warning: If the timeout is reached, a call to the function will block the main thread.
    """

    def __init__(
        self,
        function: Callable,
        timeout: float,
        max_calls: int,
        safety_net: bool,
    ):
        """
        :param function: The function to debounce.
        :param timeout: Time span, in seconds.
        :max_calls: Number of times the function is allowed to be executed within ``timeout``.
        :safety_net: Whether to remove 5% from the timeout, 'just to be sure'.
        """

        self._function = function
        self._timeout = timeout if not safety_net else 0.95 * timeout
        self._ticks = collections.deque(maxlen=max_calls)

        functools.update_wrapper(function, self)

    def __call__(self, *args, **kwargs):
        current = time.monotonic()
        # Remove the ticks that exceed the timeout.
        # Note: bisection is not an option as deques do not support slicing.
        while self._ticks and current - self._ticks[0] >= self._timeout:
            self._ticks.popleft()

        # If the queue is still full, wait
        if len(self._ticks) == self._ticks.maxlen:
            delay = self._ticks[0] + self._timeout - current
            # print(f"Waiting for {delay:.2f}s")
            time.sleep(delay)
            self._ticks.popleft()

        self._ticks.append(time.monotonic())

        return self._function(*args, **kwargs)


def debounce(*, timeout: float, max_calls: int, safety_net: bool = False) -> Callable:
    def wrapper(function: Callable):
        return Debouncer(function, timeout, max_calls, safety_net)

    return wrapper
