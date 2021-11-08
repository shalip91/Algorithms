import math
import random
from copy import deepcopy
from functools import wraps

import numpy as np
import matplotlib.pyplot as plt


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


class TSPPath:
    def __init__(self, mat, start_node_idx) -> None:
        super().__init__()
        self.start_node_idx = start_node_idx
        self.path = self.__random_path(mat)
        self.weight = self.__path_weight(mat)


    def create_mutation(self, mat, swap_ratio=0.1):
        num_swaps = math.ceil(len(self.path) * swap_ratio)
        cpy = deepcopy(self)

        for _ in range(num_swaps):
            nodes_to_swap = np.random.choice(cpy.path[1:], 2, replace=False)
            cpy.__swap(nodes_to_swap)

        # calculate new weight
        cpy.weight = cpy.__path_weight(mat)
        return cpy

    def __random_path(self, mat):
        rand_permutation = np.random.permutation(mat.shape[0])
        start_location = np.where(rand_permutation == self.start_node_idx)[0][0]
        rand_permutation[0], rand_permutation[start_location] = rand_permutation[start_location], rand_permutation[0]
        return rand_permutation

    def __path_weight(self, mat):
        res = 0
        for i, _ in enumerate(self.path):
            if i == len(self.path) - 1:
                res += mat[self.path[i], self.path[0]]
            else:
                res += mat[self.path[i], self.path[i + 1]]

        return res

    def __swap(self, idxs):
        self.path[idxs[0]], self.path[idxs[1]] = \
            self.path[idxs[1]], self.path[idxs[0]]



    def __str__(self) -> str:
        result = f'cost: {self.weight}\t'
        for node in self.path:
            result += f'{node} -> '
        result += f'{self.path[0]}'
        return result


class TSPGeneticSolver:

    def __init__(self, mat,
                start_node_idx=0,
                population_size=50,
                grows_rate=1,
                num_children=2,
                swap_ratio=0.1,
                max_generations=100) -> None:
        super().__init__()
        self.mat = mat
        self.start_node_idx = start_node_idx
        self.population_size = population_size
        self.grows_rate = grows_rate
        self.num_children = num_children
        self.max_generations = max_generations
        self.swap_ratio = swap_ratio if swap_ratio > 0 else 0.001
        self.population = []
        self.solution = None
        self.best_at_each_iter = []

    @my_timer
    def solve(self):
        self.__create_population()
        while self.max_generations > 0 and len(self.population) > 1:
            # print(len(self.population))
            self.population = self.__create_new_mutated_generation()
            self.population = self.__select_best()
            self.max_generations -= 1
            self.best_at_each_iter.append(self.__best_solution().weight)
        self.solution = self.__best_solution()
        return self

    def __create_population(self):
        for _ in range(self.population_size):
            self.population.append(TSPPath(self.mat, self.start_node_idx))

    def __select_best(self):
        num_children_to_filter = math.ceil(len(self.population) // self.num_children * self.grows_rate)
        return sorted(self.population, key=lambda p: p.weight)[:num_children_to_filter]

    def __create_new_mutated_generation(self):
        children = []
        for path in self.population:
            for i in range(self.num_children):
                children.append(path.create_mutation(self.mat, swap_ratio=self.swap_ratio))
        self.population = children
        return self.population

    def __best_solution(self):
        return min(self.population, key=lambda p: p.weight)




if __name__ == '__main__':
    graph = np.random.randint(10, 100, size=(80, 80), dtype=int)
    for i in range(graph.shape[0]):
        graph[i,i] = 0
    print(graph)


    tsp_solver = TSPGeneticSolver(mat=graph,
                                  start_node_idx=0,
                                  population_size=400,
                                  grows_rate=1,
                                  swap_ratio=0,
                                  num_children=800,
                                  max_generations=100)
    tsp_solver.solve()
    print(tsp_solver.solution)
    plt.plot(tsp_solver.best_at_each_iter)
    plt.show()
