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


def reconstruct_lcs(cache, s1):
    lcs = ""
    i, j = len(cache)-1, len(cache[0])-1
    while cache[i][j] != 0:
        if cache[i-1][j] != cache[i][j] and cache[i][j-1] != cache[i][j]:
            lcs += s1[j-1]
            i, j = i - 1, j - 1
        elif cache[i-1][j] == cache[i][j]:
            i = i - 1
        elif cache[i][j-1] == cache[i][j]:
            j = j - 1

    return lcs[::-1]


def LCS(s1, s2):
    """DP of the longest common subsequence """
    cache = [[0 for _ in range(len(s1)+1)] for _ in range(len(s2)+1)]
    for i in range(len(s2)):
        for j in range(len(s1)):
            if s1[j] == s2[i]:
                cache[i+1][j+1] = cache[i][j] + 1
            else:
                cache[i+1][j+1] = max(cache[i][j+1], cache[i+1][j])

    return reconstruct_lcs(cache, s1)


@cache_dec
def lcs(X, Y, m, n):
    """DP of the longest common subsequence length"""
    if m == 0 or n == 0:
        return 0;
    elif X[m - 1] == Y[n - 1]:
        return 1 + lcs(X, Y, m - 1, n - 1);
    else:
        return max(lcs(X, Y, m, n - 1), lcs(X, Y, m - 1, n));


def longest_polindrom(str):
    max_lcs = ""
    c = ""
    for i in range(1, len(str)-1):
        s_l = str[:i]
        s_r = str[i+1:]
        curr_lcs = LCS(s_l[::-1], s_r)
        if len(curr_lcs) > len(max_lcs):
            max_lcs = curr_lcs
            c = str[i]

    return max_lcs[::-1] + c + max_lcs


print("longest polindrom is: ", longest_polindrom("wwchppkzaracyyuioter"))

