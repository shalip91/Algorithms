import numpy as np
""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""""""""""""""""""""""""""""""""
this is a Dynamic Programming solution that builds
a table of Number of elements VS the total Value
"""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""
def recunstruct_path(cache, result, elements_V, elements_W, sack_size):
    taken_items = []
    for i in range(len(elements_V), 0, -1):
        if result <= 0:
            break
        if result == cache[i - 1, sack_size]:
            continue
        else:
            taken_items.append(i - 1)
            result -= elements_V[i - 1]
            sack_size -= elements_W[i - 1]

    return taken_items[::-1]


def knapsack_nVSw(elements_W, elements_V, sack_size):
    cache = np.full((len(elements_V) + 1, sack_size + 1), 0, dtype=int)
    for i in range(1, len(elements_V) + 1):  # inventory size
        for j in range(1, sack_size + 1):  # bag size
            if elements_W[i - 1] <= j:
                cache[i][j] = max(elements_V[i - 1] + cache[i - 1][j - elements_W[i - 1]], cache[i - 1][j])
            else:
                cache[i][j] = cache[i - 1][j]

    result = cache[cache.shape[0] - 1][cache.shape[1] - 1]
    return result, recunstruct_path(cache, result, elements_V, elements_W, sack_size)



if __name__ == '__main__':
    # elements_w = [2, 1, 4, 3]
    # elements_v = [3, 3, 4, 4]
    # sack_size = 5
    #
    # elements_w = [5, 3, 8, 9]
    # elements_v = [2, 2, 1, 1]
    # sack_size = 10

    # elements_w = [2, 3, 9, 1]
    # elements_v = [9, 3, 8, 6]
    # sack_size = 12

    #prime
    # elements_w = [8, 7, 4, 1, 8]
    # elements_v = [5, 4, 6, 9, 2]
    # sack_size = 12
    elements_w = [2, 3, 9, 1]
    elements_v = [9, 3, 8, 6]
    sack_size = 12


    result, taken_idxs = knapsack_nVSw(elements_W=elements_w, elements_V=elements_v, sack_size=sack_size)
    print(result)
    print(taken_idxs)
