import math
from typing import Any
from copy import deepcopy
from itertools import product

import numpy as np

class BoardState:
    def __init__(self, mat, target=None, heuristic='mismatch') -> None:
        super().__init__()
        self.mat = mat
        self.target = target
        self.g = math.inf
        self.p = None
        self.heuristic = heuristic
        self.f = 0  # must be at end

    def __eq__(self, other) -> bool:
        return np.all(self.mat == other.mat)

    def __lt__(self, other):
        return self.f < other.f

    @property
    def h(self):
        if self.heuristic == 'mismatch':
            return np.sum(~(self.mat == self.target))
        if self.heuristic == 'manhatttan':
            return self.__manhattan_dist()
        return 0

    def __str__(self) -> str:
        return f'{self.mat}'

    def neighbors(self):
        result = []
        max_row, max_col = self.mat.shape[0], self.mat.shape[1]
        zero_i = np.where(self.mat == 0)[0][0]
        zero_j = np.where(self.mat == 0)[1][0]
        valid_idxs = list(product(list(range(max_col)), list(range(max_row))))
        if (zero_i - 1, zero_j) in valid_idxs:  # up swap
            result.append(self.__create_move_board(zero_i, zero_j, zero_i - 1, zero_j))
        if (zero_i + 1, zero_j) in valid_idxs:  # down swap
            result.append(self.__create_move_board(zero_i, zero_j, zero_i + 1, zero_j))
        if (zero_i, zero_j - 1) in valid_idxs:  # left swap
            result.append(self.__create_move_board(zero_i, zero_j, zero_i, zero_j - 1))
        if (zero_i, zero_j + 1) in valid_idxs:  # right swap
            result.append(self.__create_move_board(zero_i, zero_j, zero_i, zero_j + 1))

        return result


    def __create_move_board(self, i_at, j_at, i_to, j_to):
        cpy = deepcopy(self)
        cpy.mat[i_at, j_at], cpy.mat[i_to, j_to] = cpy.mat[i_to, j_to], cpy.mat[i_at, j_at]
        cpy.g = math.inf
        return cpy

    def __manhattan_dist(self):
        total = 0
        for num in range(1, np.size(self.mat)):
            num_i = np.argwhere(self.mat == num)[0][0]
            num_j = np.argwhere(self.mat == num)[0][1]
            target_i = np.argwhere(self.target == num)[0][0]
            target_j = np.argwhere(self.target == num)[0][1]
            total += (abs(num_i - num_j) + abs(target_i - target_j))
        return total


if __name__ == '__main__':
    target = np.array([
        [1, 2, 3],
        [8, 0, 4],
        [7, 4, 5]
    ])
    mat2 = np.array([
        [2, 8, 3],
        [1, 6, 4],
        [7, 0, 5]
    ])

    b2 = BoardState(mat2, target)
    print(b2)
    print()
    for state in b2.neighbors():
        print(state)






