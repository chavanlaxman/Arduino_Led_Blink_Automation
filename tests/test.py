import pytest
from functools import wraps
def retry(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        excep =None
        for i in range(3):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print("retrying")
        raise excep
    return wrapper


@retry
@pytest.mark.parametrize("input, output",[(1,1),(1,2)])
def test_fail(input,output):
    assert input==output