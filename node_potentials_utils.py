import networkx as nx

def initialize_phi_list(graph: nx.MultiGraph) -> dict:
    phi = {node: None for node in graph.nodes}
    return phi


def process_edf_branches(graph, phi: dict = None):
    if phi is None:
        phi = initialize_phi_list(graph)
    edf_branches = []
    for u, v, data in graph.edges(data=True):
        if len(data['elements']) == 1 and data['elements'][0]['type'] == 'ElectromotiveForce':
            edf_branches.append((u, v, data['elements'][0]['value']))
    if len(edf_branches) > 1:
        raise ValueError(
            'Найдено более одной ветви с единственным источником ЭДС, '
            'неоднозначность в определении потенциалов'
        )
    elif len(edf_branches) == 1:
        u, v, value = edf_branches[0]
        phi[u] = 0
        phi[v] = value
    else:
        first_key = list(phi.keys())[0]
        phi[first_key] = 0
    return phi



