from scheduling_package.task import Task
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


def previous_available_task(tasks_sorted_by_end):
    p = [0] * (len(tasks_sorted_by_end) + 1)

    for curr_task in tasks_sorted_by_end:
        for end_task in tasks_sorted_by_end:
            if curr_task.start < end_task.end:
                p[curr_task.name] = end_task.name - 1
                break

    return p

def single_machine_weighted(tasks):
    """calculates the maximum value of compatible tasks
       O( n )

    Args:
        tasks: list of tasks that
    Returns:
        list of copatible tasks
    """
    tasks_sorted_by_end = sorted(tasks.values(), key=lambda t: t.end)
    prev_avail_tasks = previous_available_task(tasks_sorted_by_end)

    @cache_dec
    def compute(j):
        if (j == 0):
            return 0
        else:
            return max(tasks_sorted_by_end[j-1].value + compute(prev_avail_tasks[j]),
                       compute(j-1))

    return compute(len(tasks_sorted_by_end))




if __name__ == '__main__':
    tasks = {
        1: Task(1, 1, 4, 2),
        2: Task(2, 2, 6, 4),
        3: Task(3, 5, 7, 4),
        4: Task(4, 3, 10, 7),
        5: Task(5, 8, 11, 2),
        6: Task(6, 9, 12, 1)
    }

    # for t in single_machine_weighted(tasks):
    #     print(t)

    print(single_machine_weighted(tasks))


