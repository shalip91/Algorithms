import heapq
import numpy as np
from board_state import BoardState
from functools import wraps

def my_timer(orig_fun):
    import time
    @wraps(orig_fun) #will prevent the stacking problem to occure
    def wrapper(*args, **kwargs):
        start = time.time()
        result = orig_fun(*args, **kwargs)
        time_took = time.time() - start
        print(f'{orig_fun.__name__} Run in {time_took} sec')
        return result
    return wrapper


def print_steps(src):
    result = [src]
    while src.p is not None:
        result.append(src.p)
        src = src.p

    for i, step in enumerate(result[::-1]):
        print(f'step: {i+1}\n', step, end='\n\n')

@my_timer
def a_star(start, target, epsilon=1):
    # if epsilon != 1:
    #     for v in g.get_vertices():
    #         v.weight.h *= epsilon
    start.g = 0
    open_list = [start]
    heapq.heapify(open_list)
    closed_list = []
    while open_list:
        src = heapq.heappop(open_list)
        if src == target:
            return print_steps(src)

        for dst in src.neighbors():
            dst_current_cost = src.g + 1
            if dst_current_cost < dst.g:
                dst.g = dst_current_cost
                dst.f = dst.g + dst.h*epsilon
                dst.p = src
                if dst in closed_list:
                    closed_list.remove(dst)
                    heapq.heappush(open_list, dst)
                else:
                    heapq.heappush(open_list, dst)

        closed_list.append(src)

    return None


def printt():
    print("hellp")


if __name__ == '__main__':
    target = np.array([
        [1, 2, 3],
        [8, 0, 4],
        [7, 6, 5]
    ])
    start = np.array([
        [2, 8, 3],
        [1, 6, 4],
        [7, 5, 0]
    ])
    # mat2 = np.array([
    #     [1, 2, 3],
    #     [8, 6, 4],
    #     [7, 0, 5]
    # ])

    start = BoardState(start, target=target, heuristic='mismatch')
    end = BoardState(mat=target, heuristic='mismatch')
    result = a_star(start, end, epsilon=1)