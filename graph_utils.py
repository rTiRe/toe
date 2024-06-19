import networkx as nx

def find_main_nodes(graph):
    return [node for node in graph.nodes if graph.degree(node) >= 3]


def aggregate_path_edges(graph, path):
    # Собираем рёбра между узлами на пути
    edges = []
    for i in range(len(path) - 1):
        u, v = path[i], path[i + 1]
        if graph.has_edge(u, v):
            edges.append(graph[u][v])
    return edges


def filter_and_aggregate_paths(graph, main_nodes, node1, node2):
    aggregated_edges = []
    all_paths = nx.all_simple_paths(graph, source=node1, target=node2)
    for path in all_paths:
        if all(node not in main_nodes for node in path[1:-1]):
            path_edges = aggregate_path_edges(graph, path)
            aggregated_edges.append(path_edges)
    return aggregated_edges


def aggregate_paths_between_main_nodes(graph, main_nodes):
    aggregated_edges = {}
    for i in range(len(main_nodes)):
        for j in range(i + 1, len(main_nodes)):
            node1, node2 = main_nodes[i], main_nodes[j]
            edges_list = filter_and_aggregate_paths(graph, main_nodes, node1, node2)
            if edges_list:
                aggregated_edges[(node1, node2)] = edges_list
    return aggregated_edges


def set_elements_directions(graph: nx.MultiGraph) -> nx.MultiGraph:
    for edge in graph.edges(data=True):
        u = edge[0]
        v = edge[1]
        elements = edge[2]['elements']
        for elem_num, element in enumerate(elements):
            if elem_num == 0:
                direction = element['u'] == u
            elif elem_num == len(elements) - 1:
                direction = element['v'] == v
            else:
                direction = elements[elem_num-1]['direction']
                if element['u'] != elements[elem_num-1]['v']:
                    direction = not direction
            element['direction'] = direction
    return graph


def simplify_graph(graph):
    simplified_graph = nx.MultiGraph()
    main_nodes = find_main_nodes(graph)
    for node in main_nodes:
        simplified_graph.add_node(node)
    aggregated_edges = aggregate_paths_between_main_nodes(graph, main_nodes)
    for (node1, node2), edges_list in aggregated_edges.items():
        for edges in edges_list:
            simplified_graph.add_edge(node1, node2, elements=edges)
    simplified_graph = set_elements_directions(simplified_graph)
    return simplified_graph