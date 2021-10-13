from graph_package.graph import Graph


""" getting the longest simple path """

def dfs(g, start):
    visited = [start]
    max_path = []


    def dfs_helper(src):
        nonlocal max_path, visited
        # if len(max_path) < len(visited):
            # max_path = visited.copy()

        if len(visited) == 10:
            max_path.append(visited.copy())

        for dst in g[src]:
            if dst.key not in visited:
                visited.append(dst.key)
                dfs_helper(dst.key)
                visited.pop()
                
    dfs_helper(start)

    return max_path


if __name__ == '__main__':

    graph_info = {
        0: {4: 1, 5: 1, 1: 1},
        1: {0: 1, 6: 1, 2: 1},
        2: {1: 1, 7: 1, 3: 1},
        3: {2: 1, 8: 1, 4: 1},
        4: {3: 1, 9: 1, 0: 1},
        5: {0: 1, 7: 1, 8: 1},
        6: {1: 1, 9: 1, 8: 1},
        7: {2: 1, 5: 1, 9: 1},
        8: {3: 1, 6: 1, 5: 1},
        9: {4: 1, 7: 1, 6: 1}
    }

    peterson_graph = Graph()

    for src in graph_info.keys():
        peterson_graph.add_vertex(src)

    for src, neighbors in graph_info.items():
        for dst, _ in neighbors.items():
            peterson_graph.add_edge(src, dst)

    print(peterson_graph)
    result = sum([len([path for path in dfs(peterson_graph, i)]) for i in range(10)])
    print(result)