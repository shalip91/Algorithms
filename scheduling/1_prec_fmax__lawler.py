import math
import pandas as pd
import numpy as np
from collections import defaultdict
from copy import deepcopy
from algorithms.graph.graph_package.graph import Graph



class PrecSchedule:
    def __init__(self, file_name=None, graph=None):
        if file_name is not None and graph is not None:
            self.file_name = file_name
            self.fi_list, self.pi_list, self.adj_mat = self.__init_csv()
            self.graph = self.__graph_init(graph)
            self.schedule = self.__lawler()
        # else:
        #     self.fi_list, self.pi_list, self.adj_mat = None, None, None
        #     self.graph = None
        #     self.schedule = None


    def __init_csv(self):
        data_frame = pd.read_csv(self.file_name)
        data_frame_fi = list(map(lambda x: float(x), data_frame.columns.values))
        data_frame_pi = list(map(lambda x: int(x), data_frame.iloc[0]))
        data_frame_adj_matrix = data_frame.to_numpy()[1:]
        return data_frame_fi, data_frame_pi, data_frame_adj_matrix

    def __str__(self):
        return f'{self.file_name}:\n fi_list: {self.fi_list}\n pi_list: {self.pi_list}\n adj_matrix:\n{self.adj_mat}\n'

    def __graph_init(self, graph):
        mat_graph = defaultdict(dict)
        for i in range(len(self.adj_mat)):
            for j in range(len(self.adj_mat[0])):
                if self.adj_mat[i][j] != 0:
                    mat_graph[i][j] = self.adj_mat[i][j]
        print(mat_graph)

        for src, neighbors in mat_graph.items():
            for dst in neighbors.keys():
                graph.add_edge(src, dst)
        print(graph)
        return graph

    def display_graph(self):
        print(self.graph)

    def compute_schedule(self):
        return self.schedule

    @staticmethod
    def combine_schedules(first, second, connection_mat_file_name):
        df = pd.read_csv(connection_mat_file_name, header=None)
        conn_mat = df.to_numpy()
        combined_mat = PrecSchedule.__concatenate_mats(left=first.adj_mat,
                                                       diagonal=second.adj_mat,
                                                       right=conn_mat)
        combined_fi = first.fi_list + second.fi_list
        combined_pi = first.pi_list + second.pi_list


        combined = PrecSchedule()
        g = Graph(container='list', directed=True)
        combined.fi_list, combined.pi_list, combined.adj_mat = combined_fi, combined_pi, combined_mat
        combined.graph = combined.__graph_init(g)
        combined.schedule = combined.__lawler()

        return combined.schedule


    @staticmethod
    def __concatenate_mats(left, diagonal, right):
        zeros_pad = np.zeros(shape=(diagonal.shape[0], diagonal.shape[0]), dtype=int)
        upper_mat_combine = np.concatenate((left, right), axis=1)
        lower_mat_combine = np.concatenate((zeros_pad, diagonal), axis=1)
        return np.concatenate((upper_mat_combine, lower_mat_combine))

    def __lawler(self):
        graph = deepcopy(self.graph)
        prc_times = self.pi_list.copy()
        p = sum(self.fi_list)
        s = set(self.graph.get_vertices())
        sched_res = []
        n = len(s)

        for k in range(n, 0, -1):
            f_k = math.inf
            taken_job = -1
            taken_idx = 0
            # find job j in s such that out deg is 0 and fj(p) is minimal
            for idx, job in enumerate(s):
                # check if out degree is 0
                if graph.degree(job.key)[1] == 0:
                    if f_k > (self.fi_list[job.key] * p):
                        f_k = self.fi_list[job.key] * p
                        taken_job = job
                        taken_idx = idx

            # update given data
            if taken_job != -1:
                s.remove(taken_job)
                sched_res.append(taken_job)
                p = p - prc_times[taken_idx]
                prc_times.pop(taken_idx)
                graph.remove_vertex(taken_job.key)

        # return the schedule
        return sched_res[::-1]


if __name__ == '__main__':
    g_fry = Graph(container='list', directed=True)
    fry = PrecSchedule('data/Fry.csv', g_fry)
    sched_fry = fry.compute_schedule()
    for x in sched_fry:
        print(x.key, end=' ')
    print()
    fry.display_graph()

    g_leela = Graph(container='list', directed=True)
    leela = PrecSchedule('data/Leela.csv', g_leela)
    sched_leela = leela.compute_schedule()
    for x in sched_leela:
        print(x.key, end=' ')
    print()
    leela.display_graph()

    comb = PrecSchedule.combine_schedules(fry, leela, 'data/Fry_Leela.csv')
    for x in comb:
        print(x.key, end=' ')