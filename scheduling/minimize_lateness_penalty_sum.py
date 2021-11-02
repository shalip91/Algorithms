import numpy as np


"""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""
this script will calculate the list of all the task 
that should be late in order to optimize 
the schedule in terms of total late tasks
""""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""""""""""""""""""""""""""""""""""""""


def reconstruct_schedule(table, deadline, w_penalty):
    schedule = []
    t = deadline[-1]
    for j in range(len(deadline)-1, 1, -1):
        t = min(t, deadline[j])
        # meanning that j is late
        if table[j][t] == table[j-1][t] + w_penalty[j]:
            schedule.append(j-1)
        else:
            t -= w_penalty[j]

    return schedule

def minimize_lateness(process_time, w_penalty, deadline):
    """calculate the schedule that minimizes the lateness penalty of all the tasks.

        Args:
            process_time: list of processing time of the tasks
            w_penalty: list of all the penalties for the lateness of each task
            deadline: list of deadline of the tasks

        Returns:
            list of tasks that should be considered as late.
    """

    # just padding the lists with with garbage value at the beginning
    process_time.insert(0, 0)
    w_penalty.insert(0, 0)
    deadline.insert(0, 0)

    # create the DP table with additional row at the start full of zeros.
    table = np.zeros(shape=(len(process_time), sum(process_time)+1), dtype=int)

    for j in range(1, table.shape[0]):
        # dp formula F, if negative entry for function F it is considered as inf
        for t in range(deadline[j]+1):
            if t - process_time[j] < 0 or \
                    table[j-1][t] + w_penalty[j] < table[j-1][t-process_time[j]]:
                table[j][t] = table[j-1][t] + w_penalty[j]
            else:
                table[j][t] = table[j-1][t-process_time[j]]
        # dp formula F, from t > deadline[j]
        for t in range(deadline[j]+1, sum(process_time)+1):
            table[j][t] = table[j][deadline[j]]
    print(table)
    return reconstruct_schedule(table, deadline, w_penalty)

if __name__ == "__main__":
    process_time = [3, 2, 2, 4]
    deadline = [4, 3, 6, 5]
    w_penalty = [5, 6, 2, 4]



    print(f'{minimize_lateness(process_time, w_penalty, deadline)}')
