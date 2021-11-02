import random
from collections import defaultdict
import numpy as np

"""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""
this section handle NP problems with approximations.
the idea is to find a polynomial time algorithm that approximate
the optimal result up to a certain Factor (const/non-const).
""""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""""""""""""""""""""""""""""""""""""""


class Task:
    def __init__(self, name, duration):
        self.name = name
        self.duration = duration

    def __str__(self) -> str:
        return f"{self.name}: {self.duration}"


def load_balance_approx(tasks, number_of_machines):
    """ give an approximation schedule that minimize
    the max time on the machine - try to balance the tasks
    between the machines.
    the approximation will be at most 1.5 * optimal solution.

    :param tasks: list of tasks object
    :param number_of_machines: number of machines
    :return: maximum time minimized, schedule dict
    """
    tasks = sorted(tasks, key=lambda t: t.duration, reverse=True)
    machines_time = [0] * number_of_machines
    machines_tasks = defaultdict(list)

    for task in tasks:
        min_index = np.argmin(machines_time)
        machines_time[min_index] += task.duration
        machines_tasks[min_index].append(task)

    return max(machines_time), machines_tasks


if __name__ == "__main__":
    tasks = [Task('a1', 1), Task('a2', 7), Task('a3', 4), Task('a4', 2), Task('a5', 2),
             Task('a6', 3), Task('a7', 4), Task('a8', 4), Task('a9', 5)]
    random.shuffle(tasks)

    max_time, schedule = load_balance_approx(tasks, number_of_machines=4)
    print(max_time)

    for machine_name, tasks in schedule.items():
        print(f"\nmachine ({machine_name}):   ", end="")
        for task in tasks:
            print(f"{task}\t", end="")
