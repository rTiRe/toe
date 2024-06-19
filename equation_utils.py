import networkx as nx
import numpy

class Equation:
    def __init__(self, graph: nx.MultiGraph, phi: dict) -> None:
        self.graph = graph
        self.phi = phi
        node_info_part = {node: 0 for node in graph.nodes}
        self.left_part = {node: node_info_part.copy() for node in graph.nodes}
        self.right_part = node_info_part.copy()

    def calculate_left_part(self) -> dict:
        for node, node_data in self.graph.nodes(data=True):
            left_data = self.left_part[node]
            if self.phi[node] is None:
                left_data[node] = node_data['conductivity']
            edges = self.graph.edges(node, data=True)
            for edge_u, edge_v, edge_data in edges:
                edge_conductivity = edge_data['conductivity']
                second_node = edge_u if edge_v == node else edge_v
                if self.phi[node] is None and self.phi[second_node] is None:
                    left_data[second_node] -= edge_conductivity
        return self.left_part

    def calculate_right_part(self) -> dict:
        for node, node_data in self.graph.nodes(data=True):
            # print(node_data)
            if self.phi[node] is None:
                # print('old', self.right_part)
                self.right_part[node] += node_data['emf']
                # print('new', self.right_part)
            # print(node_data)
            # print(node_data['emf'])
            self.right_part[node] += node_data['csf']
            # print(self.right_part)
        return self.right_part

    def calculate(self) -> list:
        M = numpy.array([list(value.values()) for value in self.left_part.values()])
        V = numpy.array([value for value in self.right_part.values()])
        print(M)
        print()
        print(V)
        return numpy.linalg.lstsq(M, V, rcond=None)[0]

