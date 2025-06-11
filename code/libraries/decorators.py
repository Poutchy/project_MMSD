import time
from typing import Any, Callable


def timer(func: Callable) -> Callable:
    """
    Decorator that measures and prints the execution time of a function.

    Parameters
    ----------
    func : Callable
        The function to be wrapped and timed.

    Returns
    -------
    Callable
        A wrapped version of `func` that prints how long it took to execute.
    """

    def wrapper(*args, **kwargs) -> Any:
        start_time: float = time.perf_counter()
        res: Any = func(*args, **kwargs)
        end_time: float = time.perf_counter()

        print(f'Ran "{func.__name__}" in {end_time - start_time:3f}')
        return res

    return wrapper
