import math
import pickle
from functools import wraps
import numpy as np


def cache_dec(f):
    cache = {}
    @wraps(f)
    def wrapper(*args, **kwargs):
        # using pickle to hash any objects that are not hashable
        t = (pickle.dumps(args), pickle.dumps(kwargs))
        if t not in cache:
            cache[t] = f(*args, **kwargs)
        return cache[t]
    return wrapper


@cache_dec
def fib(n):
    if n <= 2:
        return 1
    return fib(n-1) + fib(n-2)

#
# for i in range(50):
#     print(fib(i))



# @cache_dec
def rod_cut(n, c):
    prices = [0, 1, 5, 8, 9, 10, 17, 17, 20, 24, 30,
              27, 32, 32, 40, 42, 41, 47, 52, 52, 63,
              68, 69, 69, 72, 75, 76, 76, 76, 78, 81, 81]
    def rod_cut_helper(n):
        if n == 0:
            return c
        q = prices[n]
        curr_slice = -1
        for i in range(1, n+1):
            if q < prices[i] + rod_cut_helper(n-i) - c:
                q = prices[i] + rod_cut_helper(n-i) - c
                curr_slice = i
        if curr_slice != -1:
            slices.append(curr_slice)

        return q,

    return rod_cut_helper(n), slices

for i in range(1, 10):
    print(f'rod size: {i}\tresult: {rod_cut(i, 0)}')
# price, slices = rod_cut(5, 0)
# print(slices)
# print(f'rod size: {4}\tresult: {price, slices}')