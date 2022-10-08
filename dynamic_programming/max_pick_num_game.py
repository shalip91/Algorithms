import pickle
from functools import wraps

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
def game(l):
    if len(l) == 1:
        return 0

    if len(l)%2 == 0:
        return max(l[0] + game(l[1:]), l[-1] + game(l[:-1]))
    else:
        return min(game(l[1:]), game(l[:-1]))


if __name__ == '__main__':
    l = [10, 20, 5, 4]
    print(game(l))