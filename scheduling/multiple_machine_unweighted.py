from scheduling_package.task import Task
from single_machine_unweighted import single_machine_unweighted

def multiple_machine_unweighted(tasks):
    """calculates the minimum number of machines needed for all tasks
       O( n log(n) )

    Args:
        tasks: list of tasks that
    Returns:
        list of machines that contains a list of task for each machine
    """

    machine_tasks = []

    while tasks:
        machine_tasks.append(single_machine_unweighted(tasks))
        for task in machine_tasks[-1]:
            del tasks[task.name]

    return machine_tasks

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

    for machine_tasks in multiple_machine_unweighted(tasks):
        for task in machine_tasks:
            print(task)
        print()
    


