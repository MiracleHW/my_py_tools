# -*- coding: utf-8 -*-
# File  : utils.py
# Author: huwei
# Date  : 2021/4/7
import time
from functools import wraps

__all__=["except_retry","timecost"]

def except_retry(retry_nums=1, default_return=None, sleep=None):
    def retry(func):
        @wraps(func)
        def warp_func(*args, **kargs):
            for i in range(retry_nums):
                try:
                    return func(*args, **kargs)
                except Exception as e:
                    print(f"ERROR: Retry num {i} function {func.__name__} called error")
                    print(str(e))
                if sleep is not None and sleep > 0:
                    time.sleep(sleep)
            return default_return
        return warp_func
    return retry

def timecost(func):
    @wraps(func)
    def warp_func(*args, **kargs):
        start = time.time()
        res = func(*args, **kargs)
        print(f"Time cost of {func.__name__}:{time.time() - start}")
        return res
    return warp_func