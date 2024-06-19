import networkx as nx
from copy import deepcopy

def calculate_edges_conductivities(graph: nx.MultiGraph) -> nx.MultiGraph:
    for edge in graph.edges(data=True):
        elements = edge[2]['elements']
        edge_resistance = 0
        for element in elements:
            element_type = element['type']
            if element_type in ('Inductor', 'Resistor'):
                edge_resistance += element['value']
            elif element_type == 'Capacitor':
                edge_resistance -= element['value']
            if element_type == 'CurrentSource':
                edge_resistance = float(1)  # TODO: inf
                break
        if edge_resistance != 0:
            edge[2]['conductivity'] = 1 / edge_resistance
        else:
            edge[2]['conductivity'] = float(1)  # TODO: inf
    return graph


def calculate_nodes_conductivities(graph: nx.MultiGraph):
    graph = calculate_edges_conductivities(graph)
    # Расчёт проводимости для каждого узла
    for node in graph.nodes:
        total_conductivity = 0
        # Проходим по всем рёбрам, связанным с узлом
        for neighbor in graph.neighbors(node):
            edge_data = graph.get_edge_data(node, neighbor)
            # Поскольку это MultiGraph, может быть несколько рёбер между парой узлов
            for key in edge_data:
                total_conductivity += edge_data[key].get('conductivity', 0)
        # Сохраняем проводимость в атрибутах узла
        graph.nodes[node]['conductivity'] = total_conductivity
    return graph


def check_element_direction(edge_u: str, elements: list[dict], element: dict) -> bool:
    comparison_of_directions = element['direction'] == elements[0]['direction']
    if elements[0]['u'] == edge_u:
        return comparison_of_directions
    else:
        return not comparison_of_directions


def calculate_edges_source_values(
    element_name: str,
    graph: nx.MultiGraph,
    field_name: str = None,
) -> nx.MultiGraph:
    if field_name is None:
        field_name = element_name.lower() + '_value'
    for edge in graph.edges(data=True):
        elements = edge[2]['elements']
        edge_value = 0
        for element in elements:
            element_type = element['type']
            if element_type == element_name:
                # Если направлено ОТ u-вершины первого элемента на ветке, то прибавляем
                if check_element_direction(edge[0], elements, element):
                    edge_value += element['value']
                # Иначе отнимаем
                else:
                    edge_value -= element['value']
        edge[2][field_name] = {'u': elements[0]['u'], 'value': edge_value}
    return graph


def calculate_edges_emfs(graph: nx.MultiGraph) -> nx.MultiGraph:
    return calculate_edges_source_values('ElectromotiveForce', graph, 'emf')


def calculate_edges_csf(graph: nx.MultiGraph) -> nx.MultiGraph:
    return calculate_edges_source_values('CurrentSource', graph, 'csf')


def calculate_nodes_emfs(graph: nx.MultiGraph) -> nx.MultiGraph:
    for node in graph.nodes.data():
        node[1]['emf'] = 0
    # print(graph.nodes.data())
    for edge_u, edge_v, edge_data in graph.edges(data=True):
        edge_elements = edge_data['elements']
        node = edge_u if edge_elements[0]['u'] == edge_u else edge_v
        edge_emf = edge_data['emf']
        if edge_u == edge_emf['u']:
            graph.nodes[edge_u]['emf'] -= edge_emf['value'] * edge_data['conductivity']
            graph.nodes[edge_v]['emf'] += edge_emf['value'] * edge_data['conductivity']
        else:
            graph.nodes[edge_u]['emf'] += edge_emf['value'] * edge_data['conductivity']
            graph.nodes[edge_v]['emf'] -= edge_emf['value'] * edge_data['conductivity']
    return graph


def calculate_nodes_csf(graph: nx.MultiGraph) -> nx.MultiGraph:
    for node in graph.nodes.data():
        node[1]['csf'] = 0
    for edge_u, edge_v, edge_data in graph.edges(data=True):
        edge_elements = edge_data['elements']
        node = edge_u if edge_elements[0]['u'] == edge_u else edge_v
        edge_csf = edge_data['csf']
        if node == edge_csf['u']:
            graph.nodes[node]['csf'] += edge_csf['value'] 
        else:
            graph.nodes[node]['csf'] -= edge_csf['value']
    return graph


def calculate_circuit_data(graph: nx.MultiGraph) -> nx.MultiGraph:
    graph = deepcopy(graph)
    graph_with_nodes_conductivities = calculate_nodes_conductivities(graph)
    graph_with_edges_edfs = calculate_edges_emfs(graph_with_nodes_conductivities)
    graph_with_edges_current_sources = calculate_edges_csf(graph_with_edges_edfs)
    graph_with_nodes_edfs = calculate_nodes_emfs(graph_with_edges_current_sources)
    graph_with_nodes_current_sources = calculate_nodes_csf(graph_with_nodes_edfs)
    return graph_with_nodes_current_sources
