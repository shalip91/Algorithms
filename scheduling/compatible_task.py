import bisect

from scheduling_package.task import Task
from multiple_machine_unweighted import multiple_machine_unweighted


def are_compatible_tasks(tasks):
    """check if the tasks are compatible or not
       O( n log(n) )

    Args:
        tasks: list of tasks
    Returns:
        bool
    """

    start_times = [(t.start, True) for t in tasks]
    end_times = [(t.end, False) for t in tasks]
    start_end_times = sorted(start_times + end_times, key=lambda x: x[0])

    for i in range(1, len(start_end_times)):
        if start_end_times[i-1][1] == start_end_times[i][1]:
            return False

    return True


if __name__ == '__main__':
    tasks = {
        'd': Task('d', 5, 10),
        'b': Task('b', 3, 9),
        'f': Task('f', 11, 14),
        'g': Task('g', 13, 18),
        'a': Task('a', 1, 5),
        'e': Task('e', 7, 12),
        'j': Task('j', 17, 22),
        'h': Task('h', 15, 21),
        'i': Task('i', 16, 20),
        'c': Task('c', 4, 6),
        'k': Task('k', 19, 23)
    }

    # print(are_compatible_tasks(tasks))
    for machine_tasks in multiple_machine_unweighted(tasks):
        print(f'compatible tasks? -> {are_compatible_tasks(machine_tasks)}')
        for task in machine_tasks:
            print(task)
        print()

