"""Module for work with equation."""

import networkx as nx
import numpy


class Equation:
    """Class for work with equation."""

    def __init__(self, graph: nx.MultiGraph, phi: dict) -> None:
        """Initialize equation.

        Args:
            graph (MultiGraph): graph with data.
            phi (dict): dict with nodes potentials.
        """
        self.graph = graph
        self.phi = phi
        node_info_part = {node: 0 for node in graph.nodes}
        self.left_part = {node: node_info_part.copy() for node in graph.nodes}
        self.right_part = node_info_part.copy()

    def calculate_left_part(self) -> dict:
        """Calculate equation left part.

        Returns:
            dict: calcuated left part.
        """
        for node, node_data in self.graph.nodes(data=True):
            left_data = self.left_part[node]
            if self.phi[node] is None:
                left_data[node] = node_data['conductivity']
            edges = self.graph.edges(node, data=True)
            for edge_u, edge_v, edge_data in edges:
                second_node = edge_u if edge_v == node else edge_v
                if self.phi[node] is None and self.phi[second_node] is None:
                    left_data[second_node] -= edge_data['conductivity']
        return self.left_part

    def calculate_right_part(self) -> dict:
        """Clalculate right part of equation.

        Returns:
            dict: calculated right part.
        """
        for node, node_data in self.graph.nodes(data=True):
            if self.phi[node] is None:
                self.right_part[node] += node_data['emf']
            self.right_part[node] += node_data['csf']
        return self.right_part

    def calculate(self) -> list:
        """Calculate equation.

        Returns:
            list: solved equation.
        """
        equation_left = numpy.array(
            [list(left_part_value.values()) for left_part_value in self.left_part.values()],
        )
        equation_right = numpy.array(list(self.right_part.values()))
        print(equation_left)
        print()
        print(equation_right)
        return numpy.linalg.lstsq(equation_left, equation_right, rcond=None)[0]
