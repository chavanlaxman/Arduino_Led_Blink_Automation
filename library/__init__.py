
import pytest
from functools import wraps


def retry(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        last_exception =None
        for i in range(3):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"retrying -- {i}")
                last_exception =e
        raise last_exception
    return wrapper


@retry
@pytest.mark.parameterize("input, output", [(1 ,2) ,(2 ,4)])
def test_param(input, output):
    assert input + 1==output, "failed in comp"