import numpy as np
""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""""""""""""""""""""""""""""""""
this is a Dynamic Programming solution that builds
a table of Number of elements VS the total Value
"""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""
def recunstruct_path(table, elements_w, sack_size):
    i = table.shape[0]-1
    result = []
    for j in range(table.shape[1]-1, 0, -1):
        if table[i, j] <= sack_size:
            while table[i-1, j] == table[i, j]:
                i -= 1
            result.append(i-1)
            sack_size -= elements_w[i]
            i -= 1
        if sack_size < 1:
            break

    return result


def knapsack_nVSv(elements_W, elements_V, sack_size):

    max_val = max(elements_V)
    n = len(elements_V)
    cache = np.full((len(elements_W)+1, n*max_val+1), 0, dtype=int)
    cache[0, :] = max_val * 10
    elements_V.insert(0, None)
    elements_W.insert(0, None)

    if sack_size >= max_val * 10 or sack_size >= sum(elements_W[1:]):
        return cache, list(range(len(elements_W)-1))

    for i in range(1, n+1):
        for p in range(1, n*max_val+1):
            if elements_V[i] > p:
                cache[i, p] = cache[i-1, p]
            else:
                cache[i, p] = min(cache[i-1, p], elements_W[i] + cache[i-1, p-elements_V[i]])


    return cache, recunstruct_path(cache, elements_W, sack_size)



if __name__ == '__main__':
    elements_w = [2, 1, 4, 3]
    elements_v = [3, 3, 4, 4]
    sack_size = 5

    # elements_w = [5, 3, 8, 9]
    # elements_v = [2, 2, 1, 1]
    # sack_size = 10

    # elements_w = [2, 3, 9, 1]
    # elements_v = [9, 3, 8, 6]
    # sack_size = 12


    table, result = knapsack_nVSv(elements_W=elements_w, elements_V=elements_v, sack_size=sack_size)
    print(table)
    print(result)