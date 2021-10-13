import math
from graph_package.flow_graph import FlowGraph
from Flow_Ford_Fulkerson import *
import pandas as pd
from collections import defaultdict


if __name__ == '__main__':
    df = pd.read_csv('data/girls_boys.csv', header=None)
    # print(df)

    graph_input = defaultdict(dict)

    for i in range(df.shape[0]):
        for j in range(df.shape[0]):
            if df.iloc[i, j]:
                # print(f'{i} -> {j}')
                graph_input[f'boy {i}'][f'girl {j}'] = 1

    # adding source and sink
    for i in range(df.shape[0]):
        graph_input['s'][f'boy {i}'] = 1
        graph_input[f'girl {i}']['t'] = 1

    input_to_graph = dict(graph_input)
    # print(input_to_graph)
    g = FlowGraph(graph=input_to_graph)
    print(g)

    ford_fulkerson(g)
    print(g.result())

