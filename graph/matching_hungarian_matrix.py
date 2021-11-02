import math
from graph_package.flow_graph import FlowGraph
import pandas as pd
from collections import defaultdict
import numpy as np


def sub_min_row(mat):
    """step 1: subtracting the minimum of each row from the rows"""
    for i in range(mat.shape[0]):
        mat[i] -= np.min(mat[i])

def sub_min_col(mat):
    """step 2: subtracting the minimum of each col from the cols"""
    for j in range(mat.shape[1]):
        mat[:, j] -= np.min(mat[:, j])

def line_with_min_zeros(mat, marked_rows, marked_cols):
    """finds the row/col with the minimum zeros in it"""
    min_zeros_so_far = math.inf
    is_row = True
    line_idx = -1

    # checking the min zero count in rows
    for i in range(mat.shape[0]):
        if not marked_rows[i]:
            # counting only the zeros that are in unmarked lines
            zeros = np.count_nonzero(mat[i][~marked_cols] == 0)
            if 0 < zeros < min_zeros_so_far:
                min_zeros_so_far = zeros
                line_idx = i

    # checking the min zero count in rows
    for j in range(mat.shape[1]):
        if not marked_cols[j]:
            # counting only the zeros that are in unmarked lines
            zeros = np.count_nonzero(mat[:, j][~marked_rows] == 0)
            if 0 < zeros < min_zeros_so_far:
                is_row = False
                min_zeros_so_far = zeros
                line_idx = j

    return is_row, line_idx

def mark_lines(mat, is_row, line_idx, marked_rows, marked_cols):
    """marks all the perpendicular lines of the line that containing the zeros"""
    if is_row:
        zeros_idxs = np.where(mat[line_idx] == 0)[0]
        marked_cols[zeros_idxs] = True
    else:
        zeros_idxs = np.where(mat[:, line_idx] == 0)[0]
        marked_rows[zeros_idxs] = True

def coverage_zero_lines(mat):
    """step 3: finds the min number of lines that cover all the zeros"""
    marked_rows = np.array([False] * mat.shape[0])
    marked_cols = np.array([False] * mat.shape[1])

    while True:
        is_row, line_idx = line_with_min_zeros(mat, marked_rows, marked_cols)
        if line_idx == -1:
            break
        mark_lines(mat, is_row, line_idx, marked_rows, marked_cols)

    return marked_rows, marked_cols

def shift_zeros(mat, marked_row, marked_col):
    """step 4: find the min element out of the uncovers elements,
       subtracting it from the rest uncovered,
       add the min to all the elements that are crossed by 2 lines. """

    unmarked_row = np.arange(mat.shape[0])[~marked_row]
    unmarked_col = np.arange(mat.shape[0])[~marked_col]

    min_value = np.min(mat[unmarked_row, :][:, unmarked_col])

    # subtruct the min from all the unmarked elements
    for i in unmarked_row:
        for j in unmarked_col:
            mat[i][j] -= min_value

    # add the min to all the cross marked elements
    for i in list(set(range(mat.shape[0])) - set(unmarked_row)):
        for j in list(set(range(mat.shape[1])) - set(unmarked_col)):
            mat[i][j] += min_value


def first_unmarked_zero(mat, line_idx, valid_idxs):
    zeros_idxs = np.where(mat[line_idx] == 0)[0]
    for idx in zeros_idxs:
        if valid_idxs[idx]:
            return idx

def mark_row_col(mat, is_row, line_idx, marked_rows, marked_cols, matches):
    """marks all the rows and cols of the first zero in the line """
    if is_row:
        if not marked_rows[line_idx]:
            # if there are multiple zeros choose the first one
            zero_idx = first_unmarked_zero(mat, line_idx, ~marked_cols)

            matches.append((line_idx, zero_idx))
            marked_cols[zero_idx] = True
            marked_rows[line_idx] = True
    else:
        if not marked_cols[line_idx]:
            # if there are multiple zeros choose the first one
            zero_idx = first_unmarked_zero(mat, line_idx, ~marked_rows)

            matches.append((zero_idx, line_idx))
            marked_cols[line_idx] = True
            marked_rows[zero_idx] = True


def final_assignment(mat):
    """step 5: assigning the zeros at each"""
    marked_rows = np.array([False] * mat.shape[0])
    marked_cols = np.array([False] * mat.shape[1])
    matches = []
    while True:
        is_row, line_idx = line_with_min_zeros(mat, marked_rows, marked_cols)
        if line_idx == -1:
            break
        mark_row_col(mat, is_row, line_idx, marked_rows, marked_cols, matches)

    return matches

def munkres_matrix(mat):
    """assign each worker to task such that the total cost
       of of the task will be minimized

        Args:
            mat: matrix of number
        Returns:
            list of tuple pairs of matching (worker, task)
    """

    # copy to avoid inplace changes to the original matrix
    processing_matrix = mat.copy()
    # step 1 - subtracting the minimum of each row from the rows
    sub_min_row(processing_matrix)
    print("sub row", processing_matrix, sep='\n')

    # step 2 - subtracting the minimum of each col from the cols
    sub_min_col(processing_matrix)
    print("sub col", processing_matrix, sep='\n')

    # step 3 - while coverage line of zeros is less then matrix size
    marked_row, marked_col = coverage_zero_lines(processing_matrix)
    print(f'row: {marked_row}\ncol: {marked_col}')
    i = 1
    while (sum(marked_row) + sum(marked_col)) != mat.shape[0]:

        # go to step 4 - shift zeros + step 3 again.
        shift_zeros(processing_matrix, marked_row, marked_col)
        print("after shift", processing_matrix, sep='\n')

        marked_row, marked_col = coverage_zero_lines(processing_matrix)
        print(f'row: {marked_row}\ncol: {marked_col}')


    # step 5 - make the final assignment of task to each worker
    return final_assignment(processing_matrix)



if __name__ == '__main__':

    # mat = np.random.randint(0,80, size=(15, 15))
    mat = np.array([
        [99999, 32, 72, 128],
        [99999, 99999, 14.7, 22.6],
        [21, 28, 72, 56],
        [99999, 99999, 99999, 20]
    ])
    pairs = munkres_matrix(mat)
    summer_time = 0
    for i, j in pairs:
        summer_time += mat[i][j]

    print(mat, pairs, summer_time, sep='\n\n')



