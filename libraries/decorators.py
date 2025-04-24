import time
from typing import Any, Callable


def timer(func: Callable) -> Callable:

    def wrapper(*args, **kwargs) -> Any:
        start_time: float = time.perf_counter()
        res: Any = func(*args, **kwargs)
        end_time: float = time.perf_counter()

        print(f'Ran "{func.__name__}" in {end_time - start_time:3f}')
        return res

    return wrapper
