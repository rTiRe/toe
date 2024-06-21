"""Module for work with circuit."""

from copy import deepcopy

import networkx as nx

VALUE_LITERAL = 'value'
CONDUCTIVITY = 'conductivity'
U_LITERAL = 'u'
EMF = 'emf'
CSF = 'csf'


def calculate_edges_conductivities(graph: nx.MultiGraph) -> nx.MultiGraph:
    """Calculate conductivities for every edge.

    Args:
        graph (MultiGraph): graph for calculate conductivities.

    Returns:
        MultiGraph: graph with calculated edges conductivities.
    """
    for edge in graph.edges(data=True):
        elements = edge[2]['elements']
        edge_resistance = 0
        for element in elements:
            element_type = element['type']
            if element_type in {'Inductor', 'Resistor'}:
                edge_resistance += element[VALUE_LITERAL]
            elif element_type == 'Capacitor':
                edge_resistance -= element[VALUE_LITERAL]
            if element_type == 'CurrentSource':
                edge_resistance = float(1)  # TODO: inf
                break
        if edge_resistance == 0:
            edge[2][CONDUCTIVITY] = float(1)  # TODO: inf
        else:
            edge[2][CONDUCTIVITY] = 1 / edge_resistance
    return graph


def calculate_nodes_conductivities(graph: nx.MultiGraph) -> nx.MultiGraph:
    """Calculate conductivities for every node.

    Args:
        graph (MultiGraph): graph for calculate conductivities.

    Returns:
        MultiGraph: graph with calculated nodes conductivities.
    """
    graph = calculate_edges_conductivities(graph)
    for node in graph.nodes:
        total_conductivity = 0
        for neighbor in graph.neighbors(node):
            edge_data = graph.get_edge_data(node, neighbor)
            total_conductivity = sum(
                edge_data[key].get(CONDUCTIVITY, 0) for key in edge_data
            )
        graph.nodes[node][CONDUCTIVITY] = total_conductivity
    return graph


def check_element_direction(edge_u: str, elements: list[dict], element: dict) -> bool:
    """Check element direction.

    Args:
        edge_u (str): edge u value.
        elements (list[dict]): list of the node elements.
        element (dict): current element for calculate direction.

    Returns:
        bool: True if element direction from u node to v node.
    """
    comparison_of_directions = element['direction'] == elements[0]['direction']
    if elements[0][U_LITERAL] == edge_u:
        return comparison_of_directions
    return not comparison_of_directions


def calculate_edges_source_values(
    element_name: str,
    graph: nx.MultiGraph,
    field_name: str = None,
) -> nx.MultiGraph:
    """Calculate sum source value for every edge.

    Args:
        element_name (str): element name for found.
        graph (MultiGraph): graph for work.
        field_name (str): name of the field for paste. Defaults to None.

    Returns:
        MultiGraph: processed graph.
    """
    if field_name is None:
        field_name = f'{element_name.lower()}_value'
    for edge in graph.edges(data=True):
        elements = edge[2]['elements']
        edge_value = 0
        for element in elements:
            element_type = element['type']
            if element_type == element_name:
                if check_element_direction(edge[0], elements, element):
                    edge_value += element[VALUE_LITERAL]
                else:
                    edge_value -= element[VALUE_LITERAL]
        edge[2][field_name] = {'u': elements[0][U_LITERAL], 'value': edge_value}
    return graph


def calculate_edges_emfs(graph: nx.MultiGraph) -> nx.MultiGraph:
    """Calculate electromotive forces for every edge.

    Args:
        graph (MultiGraph): graph for work.

    Returns:
        MultiGraph: processed graph.
    """
    return calculate_edges_source_values('ElectromotiveForce', graph, EMF)


def calculate_edges_csfs(graph: nx.MultiGraph) -> nx.MultiGraph:
    """Calculate current source forces for every edge.

    Args:
        graph (MultiGraph): graph for work.

    Returns:
        MultiGraph: processed graph.
    """
    return calculate_edges_source_values('CurrentSource', graph, CSF)


def calculate_nodes_emfs(graph: nx.MultiGraph) -> nx.MultiGraph:
    """Calculate electromotive forces for every node.

    Args:
        graph (MultiGraph): graph for work.

    Returns:
        MultiGraph: processed graph.
    """
    for node in graph.nodes.data():
        node[1][EMF] = 0
    for edge_u, edge_v, edge_data in graph.edges(data=True):
        edge_emf = edge_data[EMF]
        if edge_u == edge_emf[U_LITERAL]:
            graph.nodes[edge_u][EMF] -= edge_emf[VALUE_LITERAL] * edge_data[CONDUCTIVITY]
            graph.nodes[edge_v][EMF] += edge_emf[VALUE_LITERAL] * edge_data[CONDUCTIVITY]
        else:
            graph.nodes[edge_u][EMF] += edge_emf[VALUE_LITERAL] * edge_data[CONDUCTIVITY]
            graph.nodes[edge_v][EMF] -= edge_emf[VALUE_LITERAL] * edge_data[CONDUCTIVITY]
    return graph


def calculate_nodes_csfs(graph: nx.MultiGraph) -> nx.MultiGraph:
    """Calculate current source forces for every node.

    Args:
        graph (MultiGraph): graph for work.

    Returns:
        MultiGraph: processed graph.
    """
    for node in graph.nodes.data():
        node[1][CSF] = 0
    for edge_u, edge_v, edge_data in graph.edges(data=True):
        edge_elements = edge_data['elements']
        nearest_node = edge_u if edge_elements[0][U_LITERAL] == edge_u else edge_v
        edge_csf = edge_data[CSF]
        if nearest_node == edge_csf[U_LITERAL]:
            graph.nodes[nearest_node][CSF] += edge_csf[VALUE_LITERAL]
        else:
            graph.nodes[nearest_node][CSF] -= edge_csf[VALUE_LITERAL]
    return graph


def calculate_circuit_data(graph: nx.MultiGraph) -> nx.MultiGraph:
    """Calculate circuit data and fill graph.

    Args:
        graph (MultiGraph): graph for calculate data

    Returns:
        MultiGraph: graph with calculated data.
    """
    graph = deepcopy(graph)
    graph_with_nodes_conductivities = calculate_nodes_conductivities(graph)
    graph_with_edges_edfs = calculate_edges_emfs(graph_with_nodes_conductivities)
    graph_with_edges_current_sources = calculate_edges_csfs(graph_with_edges_edfs)
    graph_with_nodes_edfs = calculate_nodes_emfs(graph_with_edges_current_sources)
    return calculate_nodes_csfs(graph_with_nodes_edfs)
