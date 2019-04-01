import datetime
import time


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)

        return instances[cls]

    return get_instance


def timeit():
    def decorator(function):
        def wrapper(*args, **kw):
            ts = time.time()
            result = function(*args, **kw)
            te = time.time()

            print((te - ts) * 1000)

            return result
        return wrapper
    return decorator
