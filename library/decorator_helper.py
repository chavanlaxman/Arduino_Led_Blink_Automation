import pytest
from functools import wraps

def retry(times=3):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None

            for i in range(times):
                try:
                    print(f"Attempt {i + 1}")
                    return func(*args, **kwargs)
                except AssertionError as e:
                    last_exception = e
                    print("Retrying...")

            # Fail test after retries
            raise last_exception
        return wrapper
    return decorator

@retry()
@pytest.mark.parametrize("input, output", [(1, 3),(2,3)])
def test_fail(input, output):
    assert input + 1 == output, "failed in comparison"


