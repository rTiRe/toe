"""Module for work with dict of nodes potentials."""

import networkx as nx


def initialize_phi_list(graph: nx.MultiGraph) -> dict:
    """Init potentials dict.

    Args:
        graph (MultiGraph): graph for find nodes.

    Returns:
        dict: nodes and None potentials.
    """
    return {node: None for node in graph.nodes}


def process_edf_branches(graph: nx.MultiGraph, phi: dict = None) -> dict:
    """Fill dict zero potentials.

    Args:
        graph (MultiGraph): graph for find potentials.
        phi (dict): dict of potentials. Defaults to None.

    Raises:
        ValueError: if graph contains more than one branch with only Electromotive Force.

    Returns:
        dict: calculated zero potentials.
    """
    if phi is None:
        phi = initialize_phi_list(graph)
    edf_branches = []
    for element_u, element_v, edge_data in graph.edges(data=True):
        element_type = edge_data['elements'][0]['type']
        if len(edge_data['elements']) == 1 and element_type == 'ElectromotiveForce':
            edf_branches.append(
                (element_u, element_v, edge_data['elements'][0]['value']),
            )
    if len(edf_branches) > 1:
        raise ValueError(
            'Найдено более одной ветви с единственным источником ЭДС, ',
            'неоднозначность в определении потенциалов',
        )
    elif len(edf_branches) == 1:
        phi[edf_branches[0][0]] = 0
        phi[edf_branches[0][1]] = edf_branches[0][2]
    else:
        first_key = list(phi.keys())[0]
        phi[first_key] = 0
    return phi
