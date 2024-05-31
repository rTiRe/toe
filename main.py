import numpy
import networkx as nx


def read_elements(filename):
    graph = nx.Graph()
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split()
            element_type = parts[0]
            node1 = parts[1]
            node2 = parts[2]
            if element_type != "Wire":
                element_name = parts[3]
                element_value = float(parts[4])
                graph.add_edge(node1, node2, from_node=node1, to_node=node2, type=element_type, name=element_name, value=element_value)
            else:
                graph.add_edge(node1, node2, from_node=node1, to_node=node2, type=element_type)
    return graph


def find_nodes(graph):
    return [node for node in graph.nodes if graph.degree(node) >= 3]


def simplify_graph(graph, nodes):
    # print(nodes)
    simplified_graph = nx.MultiGraph()
    # Добавляем узлы в упрощенный граф
    for node in nodes:
        simplified_graph.add_node(node)
    # Для каждой пары узлов найдем все пути и определим, какие из них не проходят через другие узлы
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            node1 = nodes[i]
            node2 = nodes[j]
            # print(node1, node2)
            all_paths = list(nx.all_simple_paths(graph, node1, node2))
            # print()
            # print(all_paths)
            for path in all_paths:
                if not (set(nodes) - {node1, node2}) & set(path[1:-1]):
                    # print(path)
                    path_elements = []
                    # Анализируем все ребра между последовательными точками в пути
                    for k in range(len(path) - 1):
                        current_node = path[k]
                        next_node = path[k + 1]
                        # Получаем данные о ребре между этими точками
                        edge_data = graph.get_edge_data(current_node, next_node)
                        if edge_data:
                            element_data = {
                                'from_node': edge_data['from_node'],
                                'to_node': edge_data['to_node'],
                                'type': edge_data['type'],
                                'name': edge_data.get('name', None),
                                'value': edge_data.get('value', None)
                            }
                            # Определение направления для источников тока и ЭДС
                            if element_data['type'] in ['ElectromotiveForce', 'CurrentSource']:
                                element_data['direction'] = (element_data['from_node'] == current_node and element_data['to_node'] == next_node)
                            path_elements.append(element_data)
                    # Если в пути между узлами есть элементы, сохраняем их в упрощенном графе
                    if path_elements:
                        # print('pe', path_elements)
                        simplified_graph.add_edge(node1, node2, elements=path_elements)
    return simplified_graph


def calculate_conductances(graph: nx.MultiGraph):
    conductance_sum = {key: 0 for key in graph.nodes}
    for node in graph.nodes():
        total_conductance = 0
        # Перебираем все ребра, соединенные с данным узлом
        for neighbor in graph.neighbors(node):
            for num in range(graph.number_of_edges(node, neighbor)):
                edge_data = graph.get_edge_data(node, neighbor, num)
                if 'elements' in edge_data:
                    # Перебираем все элементы на пути между узлами
                    for element in edge_data['elements']:
                        if element['type'] == 'Resistor':
                            # Добавляем проводимость резистора
                            total_conductance += 1 / element['value']
        # Сохраняем сумму проводимостей для узла
        conductance_sum[node] += total_conductance
    return conductance_sum


def calculate_branch_conductances(graph):
    branch_conductances = {}
    for node in graph.nodes():
        branch_conductances[node] = {}
        # Перебираем всех соседей текущего узла
        for neighbor in graph.neighbors(node):
            total_conductance = 0
            for num in range(graph.number_of_edges(node, neighbor)):
                edge_data = graph.get_edge_data(node, neighbor, num)
                if 'elements' in edge_data:
                    # Перебираем все элементы на этом ребре
                    for element in edge_data['elements']:
                        if element['type'] == 'Resistor':
                            total_conductance += 1 / element['value']
                    # Записываем проводимость для данной ветви
                    branch_conductances[node][neighbor] = total_conductance
    return branch_conductances


def calculate_emf_contribution(graph, branch_conductances):
    emf_contributions = {}
    for node in graph.nodes():
        emf_sum = 0
        # Перебираем всех соседей текущего узла
        for neighbor in graph.neighbors(node):
            for num in range(graph.number_of_edges(node, neighbor)):
                edge_data = graph.get_edge_data(node, neighbor, num)
                if 'elements' in edge_data:
                    # Перебираем все элементы на этом ребре
                    for element in edge_data['elements']:
                        if element['type'] == 'ElectromotiveForce':
                            if neighbor in emf_contributions.keys() and emf_contributions[neighbor] != 0:
                                if element['direction']:  # True, если направление от node к neighbor
                                    emf_value = element['value']
                                else:
                                    emf_value = -element['value']
                            else:
                                # Используем поле 'direction' для определения направления ЭДС
                                if not element['direction']:  # True, если направление от node к neighbor
                                    emf_value = element['value']
                                else:
                                    emf_value = -element['value']
                            # Получаем проводимость для этой ветви
                            branch_conductance = branch_conductances[node].get(neighbor, 0)
                            # Умножаем проводимость на ЭДС и добавляем к сумме
                            emf_sum += branch_conductance * emf_value
        # Сохраняем сумму проводимостей умноженных на ЭДС для узла
        emf_contributions[node] = emf_sum
    return emf_contributions


def calculate_current_sources_contribution(graph):
    current_contributions = {}
    for node in graph.nodes():
        current_sum = 0
        # Перебираем всех соседей текущего узла
        for neighbor in graph.neighbors(node):
            for num in range(graph.number_of_edges(node, neighbor)):
                edge_data = graph.get_edge_data(node, neighbor, num)
                if 'elements' in edge_data:
                    # Перебираем все элементы на этом ребре
                    for element in edge_data['elements']:
                        if element['type'] == 'CurrentSource':
                            # Определяем направление источника тока
                            if neighbor in current_contributions.keys() and current_contributions[neighbor] != 0:
                                if element['direction']:  # True, если направление от node к neighbor
                                    current_value = element['value']
                                else:
                                    current_value = -element['value']
                            else:
                                # Используем поле 'direction' для определения направления ЭДС
                                if not element['direction']:  # True, если направление от node к neighbor
                                    current_value = element['value']
                                else:
                                    current_value = -element['value']
                            # Суммируем токи, учитывая направление
                            current_sum += current_value
        # Сохраняем сумму токов для узла
        current_contributions[node] = current_sum
    return current_contributions


def initialize_phi(graph):
    phi = {node: None for node in graph.nodes()}
    return phi


def process_edf_branches(graph, phi):
    edf_branches = []
    # Ищем ветви, содержащие только источник ЭДС
    for u, v, data in graph.edges(data=True):
        if 'elements' in data and len(data['elements']) == 1 and data['elements'][0]['type'] == 'ElectromotiveForce':
            edf_branches.append((u, v, data['elements'][0]['value']))

    # Проверяем условия на количество таких ветвей
    if len(edf_branches) > 1:
        raise ValueError("Найдено более одной ветви с единственным источником ЭДС, неоднозначность в определении потенциалов")
    elif len(edf_branches) == 1:
        # Определяем направление ЭДС и устанавливаем потенциалы
        u, v, value = edf_branches[0]
        phi[u] = 0
        phi[v] = value
    elif len(edf_branches) == 0 and None in phi.values():
        # Если нет ветвей с источником ЭДС, зануляем первый попавшийся узел
        for node in phi:
            if phi[node] is None:
                phi[node] = 0
                break
    return phi


# Замените 'path_to_your_file.txt' на путь к вашему файлу с данными
filename = 'examples/circuit1'
graph = read_elements(filename)
nodes = find_nodes(graph)
simplified_graph = simplify_graph(graph, nodes)
# for data in simplified_graph.edges(data=True):
#     print(data)
# print(simplified_graph.edges)
# print(simplified_graph.number_of_edges('5', '9'))
# print(simplified_graph.get_edge_data('5', '9', 0))
conductances = calculate_conductances(simplified_graph)
branch_conductances = calculate_branch_conductances(simplified_graph)
emf_contribution = calculate_emf_contribution(simplified_graph, branch_conductances)
current_sources_contribution = calculate_current_sources_contribution(simplified_graph)

# print(conductances)
# print()
# print(branch_conductances)
# print()
# print(emf_contribution)
# print()
# print(current_sources_contribution)

phi = initialize_phi(simplified_graph)
phi = process_edf_branches(simplified_graph, phi)
# print()
# print(phi)

left = {key: {key: 0 for key in phi.keys()} for key in phi.keys()}
right = {key: 0 for key in phi.keys()}

left_to_right= []
for node, value in phi.items():
    if value != None:
        continue
    sub_left = left[node]
    sub_left[node] = conductances[node]
    for branch_node, branch_value in branch_conductances[node].items():
        if phi[branch_node] != None:
            right[node] += (-branch_value * phi[branch_node])
            continue
        sub_left[branch_node] = -branch_value
    left[node] = sub_left
    right[node] += (emf_contribution[node] + current_sources_contribution[node])
# print(left)
# print(right)

M = numpy.array([list(value.values()) for value in left.values()])
V = numpy.array([value for value in right.values()])
# print(M)
# print(V)
result = numpy.linalg.lstsq(M, V, rcond=None)[0]
for id, key in enumerate(list(phi.keys())):
    if phi[key] == None:
        phi[key] = result[id]
print(phi)

while True:
    phi_input = input('phi\'s: ').split(' ')
    # print(phi_input)
    if phi_input[0] == 'exit':
        break
    first_phi, second_phi = phi_input
    # print(first_phi, second_phi)
    all_elements_between_two_nodes = simplified_graph.get_edge_data(first_phi, second_phi)
    # print(simplified_graph.get_edge_data(first_phi, second_phi))
    electromotive_force_for_i = 0
    resistance_for_i = 0
    for value in all_elements_between_two_nodes.values():
        # print(value)
        elem_group = value['elements']
        for elem in elem_group:
            if elem['type'] == 'ElectromotiveForce':
                electromotive_force_direction = elem['direction']
                if elem_group[0]['from_node'] != first_phi:
                    electromotive_force_direction = not electromotive_force_direction
                electromotive_force_for_i += elem['value'] if electromotive_force_direction else -elem['value']
        resistance_for_i += sum([elem['value'] for elem in elem_group if elem['type'] == 'Resistor'])
    # print(electromotive_force_for_i)
    # print(resistance_for_i)
    i = (phi[first_phi] - phi[second_phi] + electromotive_force_for_i)/resistance_for_i
    print(i)

# TODO хз как считаются токи для параллельных веток (выходят из одной точки и входят в одну точку)