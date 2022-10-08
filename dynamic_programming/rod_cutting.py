import math
import pickle
from functools import wraps
from collections import defaultdict


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


def rod_cut(n, c):
    prices = [0, 1, 5, 8, 9, 10, 17, 17, 20, 24, 30,
              27, 32, 32, 40, 42, 41, 47, 52, 52, 63,
              68, 69, 69, 72, 75, 76, 76, 76, 78, 81, 81]
    cache = [-math.inf for _ in range(n + 1)]
    cache_rod_cuts = [[] for _ in range(n + 1)]

    def rod_cut_helper(n):
        if cache[n] >= 0:
            return cache[n]

        if n <= 0:
            return c
        q = -math.inf
        min_idx = -1
        for i in range(1, n + 1):
            if q < prices[i] + rod_cut_helper(n - i) - c:
                q = prices[i] + rod_cut_helper(n - i) - c
                min_idx = i
        cache[n] = q

        if min_idx == n:
            cache_rod_cuts[n].append(min_idx)
        else:
            cache_rod_cuts[n] = cache_rod_cuts[min_idx] + cache_rod_cuts[n - min_idx]

        return q

    rod_cut_helper(n)

    res = defaultdict(int)
    for cut in cache_rod_cuts[n]:
        res[cut] += 1

    return cache[n], res


for i in range(1, 30):
    print(f'rod size: {i}\tresult: {rod_cut(i, 0)}')