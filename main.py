import pprint

class Circuit:
    def __init__(self, connections):
        self._circuit = dict()
        self.add_connections(connections)

    def add_connections(self, connections):
        for node1, node2 in connections:
            self.add(node1, node2)

    def __add__(self, nodes: tuple[int]) -> None:
        """ Magic Add connection between node1 and node2 """
        if len(nodes) > 2:
            raise ValueError('Too much elements')
        self.add(nodes[0], nodes[1])

    def add(self, node1, node2):
        """ Add connection between node1 and node2 """
        for node in (node1, node2):
            if node not in self._circuit:
                self._circuit[node] = set()
        self._circuit[node1].add(node2)
        self._circuit[node2].add(node1)

    def __dfs_util(self, node: int, visited: set):
        visited.add(node)
        for neighbour in self._circuit[node]:
            if neighbour not in visited:
                self.dfs_util(neighbour, visited)

    def dfs(self, node: int):
        visited = set()
        self.__dfs_util(node, visited)

    def __str__(self):
        return f'{dict(self._circuit)}'
    
    def __len__(self):
        return len(self._circuit)
    
    def find_cycles(self):
        cycles = []

        def dfs(node, parent, current_path, visited):
            visited[node] = True
            current_path.append(node)
            for neighbor in self._circuit[node]:
                if neighbor == parent:
                    continue
                if neighbor in current_path:
                    cycle_start_index = current_path.index(neighbor)
                    cycle = current_path[cycle_start_index:]
                    cycles.append(cycle)
                elif not visited[neighbor]:
                    dfs(neighbor, node, current_path, visited)
            current_path.pop()
            visited[node] = False 

        visited = {n: False for n in self._circuit}
        for node in self._circuit:
            dfs(node, None, [], visited)

        return cycles

connections = [(1, 2), (2, 3), (3, 4),
                (4, 1), (3, 5), (5, 6), (6, 4)]
g = Circuit(connections)
# g + (6, 4)
print(g)
cycles = g.find_cycles()
cycles_set = set()
for elem in cycles:
    cycles_set.add(tuple(elem))
cycles = list(filter(lambda x: len(x) > 2, list(cycles_set)))
print(sorted(cycles))