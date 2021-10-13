from scheduling_package.task import Task

def single_machine_unweighted(tasks):
    """calculates the maximum number of compatible tasks
       O( n log(n) )

    Args:
        tasks: list of tasks that
    Returns:
        list of copatible tasks
    """

    sorted_tasks_by_end = sorted(tasks.values(), key=lambda t: t.end)
    max_compatible_tasks = [sorted_tasks_by_end[0]]

    for task in sorted_tasks_by_end[1:]:
        if task.start > max_compatible_tasks[-1].end:
            max_compatible_tasks.append(task)

    return max_compatible_tasks


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

    for task in single_machine_unweighted(tasks):
        print(task)
    


