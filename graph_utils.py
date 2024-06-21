"""Module for work with circuit graph."""

import networkx as nx


def find_main_nodes(graph: nx.MultiGraph) -> list:
    """Find nodes with three or mode connected edges.

    Args:
        graph (MultiGraph): graph for find nodes.

    Returns:
        list: nodes with three or mode connected edges.
    """
    return [node for node in graph.nodes if graph.degree(node) >= 3]


def aggregate_path_edges(graph: nx.MultiGraph, path: list | tuple) -> list:
    """Aggregate path edges.

    Args:
        graph (MultiGraph): graph for work.
        path (list | tuple): path for aggregate.

    Returns:
        list: aggregated path.
    """
    edges = []
    for path_number in range(len(path) - 1):
        u_node = path[path_number]
        v_node = path[path_number + 1]
        if graph.has_edge(u_node, v_node):
            edges.append(graph[u_node][v_node])
    return edges


def filter_and_aggregate_paths(
    graph: nx.MultiGraph,
    main_nodes: list | tuple,
    nodes: list | tuple,
) -> list:
    """Filter and aggregate pathes.

    Args:
        graph (MultiGraph): graph for work.
        main_nodes (list | tuple): nodes for aggregate paths.
        nodes (list | tuple): source and target nodes.

    Returns:
        list: _description_
    """
    aggregated_edges = []
    source_node, target_node = nodes
    all_paths = nx.all_simple_paths(graph, source=source_node, target=target_node)
    for path in all_paths:
        if all(node not in main_nodes for node in path[1:-1]):
            path_edges = aggregate_path_edges(graph, path)
            aggregated_edges.append(path_edges)
    return aggregated_edges


def aggregate_paths_between_main_nodes(graph: nx.MultiGraph, main_nodes: list | tuple) -> dict:
    """Aggregate paths between main nodes.

    Args:
        graph (MultiGraph): graph for work.
        main_nodes (list | tuple): nodes for aggregate path between.

    Returns:
        dict: aggregated paths.
    """
    aggregated_edges = {}
    for first_node_number in range(len(main_nodes)):
        for second_node_number in range(first_node_number + 1, len(main_nodes)):
            node1, node2 = main_nodes[first_node_number], main_nodes[second_node_number]
            nodes = (node1, node2)
            edges_list = filter_and_aggregate_paths(graph, main_nodes, nodes)
            if edges_list:
                aggregated_edges[(node1, node2)] = edges_list
    return aggregated_edges


def get_element_direction(
    element: dict,
    element_number: int,
    elements: list,
    nodes: list | tuple,
) -> bool:
    """Get direction of the given element.

    Args:
        element (dict): info about element.
        element_number (int): number of the element in list.
        elements (list): list of the elements.
        nodes (list | tuple): node u and node v.

    Returns:
        bool: True if direction from u to v.
    """
    u_node, v_node = nodes
    if element_number == 0:
        direction = element['u'] == u_node
    elif element_number == len(elements) - 1:
        direction = element['v'] == v_node
    else:
        direction = elements[element_number-1]['direction']
        if element['u'] != elements[element_number-1]['v']:
            direction = not direction
    return direction


def set_elements_directions(graph: nx.MultiGraph) -> nx.MultiGraph:
    """Set direction for every element in graph.

    Args:
        graph (MultiGraph): graph for work.

    Returns:
        MultiGraph: graph with elements directions.
    """
    for edge in graph.edges(data=True):
        nodes = (edge[0], edge[1])
        elements = edge[2]['elements']
        for element_number, element in enumerate(elements):
            direction = get_element_direction(element, element_number, elements, nodes)
            element['direction'] = direction
    return graph


def simplify_graph(graph: nx.MultiGraph) -> nx.MultiGraph:
    """Save only nodes with three or more connected edgse.

    Args:
        graph (MultiGraph): graph for simplify.

    Returns:
        MultiGraph: simplified graph.
    """
    simplified_graph = nx.MultiGraph()
    main_nodes = find_main_nodes(graph)
    for node in main_nodes:
        simplified_graph.add_node(node)
    aggregated_edges = aggregate_paths_between_main_nodes(graph, main_nodes)
    for (node1, node2), edges_list in aggregated_edges.items():
        for edges in edges_list:
            simplified_graph.add_edge(node1, node2, elements=edges)
    return set_elements_directions(simplified_graph)
