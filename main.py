from elements import Element, Wire, CurrentSource, ElectromotiveForce, Resistor
from circuit import Circuit
from circuit_parser import parser
import inspect
import numpy

print('Приветствуем!')
print('Схему предстоит вводить ручками и постепенно :(')
print('Должен допилить.')

circuit = Circuit()
hand_make = False

file_path = input('Введите имя файла если хотите считать данные цепи с него [q для продолжения]: ')
if file_path == 'q':
    hand_make = True
else:
    parser(file_path, circuit)
while hand_make:
    print('\nВыберите номер элемента, который хотите добавить из списка ниже (q для продолжения):')
    elements = Element.__subclasses__()
    for num, element in enumerate(elements):
        print(f'{num+1}. {element._global_name}')
    element_num = input('Ввод: ')
    if element_num == 'q':
        break
    try:
        element_num = int(element_num)
    except ValueError:
        print('Введите число!')
        continue
    if element_num > len(elements):
        print('Такого элемента нет!')
        continue
    element = elements[element_num - 1]
    args = []
    for arg in inspect.getfullargspec(element)[0][1:]:
        args.append(input(f'Введите {arg}: '))
    element(*args)
    circuit.add_element()

# print(list(Element._elements.items())[0][1])
# print(circuit.get_points())

# print()
# mashes = circuit.get_mashes()
# if len(mashes) == 0:
#     print('Контура не были найдены.')
# else:
#     while True:
#         print()
#         print('Найдены контура:')
#         for num, mash in enumerate(mashes):
#             print(f'{num+1}. {mash}')
#         print()
#         print('Последовательность точек = направление тока в контуре')
#         mashes_to_reverse = input('Если нужно поменять направление в контурах, введите их через запятую [q для продолжения]: ').replace(' ', '').split(',')
#         if mashes_to_reverse[0] == 'q':
#             break
#         for mash in mashes_to_reverse:
#             circuit.reverse_mash(int(mash)-1)

print()
print()
nodes = circuit.get_nodes()
if len(nodes) == 0:
    print('Узлы не были найдены.')
else:
    print('Найдены узлы:')
    for num, (node, connected_nodes) in enumerate(nodes.items()):
        print(f'{num+1}. {node}: {[f"{sub_node}: {[str(element) for element in elements]}" for sub_node, elements in connected_nodes.items()]}')
# print(circuit.get_element(2, 1).name, circuit.get_element(1, 2).get_nodes())

phi = {node: None for node in nodes.keys()}

#
# СМОТРИМ НАПРАВЛЕНИЕ ElectromotiveForce ДЛЯ КАЖДОГО НАЙДЕНОГО,
# ТОЛЬКО ЕСЛИ ОН ОДИН В ВЕТКЕ
#
element_class = ElectromotiveForce
positive_directions = []
negative_directions = []
for node, connected_nodes in circuit.find_nodes_with_element(element_class).items():
    for sub_node, elements in connected_nodes.items():
        elements = list(filter(lambda x: not isinstance(x, Wire), elements))
        if len(elements) == 1:
            element: Element = elements[0]
            # print(node, sub_node, element.name)
            element_direction = circuit.get_element_direction(node, element, element.node1)
            # print(node, element.name, element_direction)
            if element_direction:
                positive_directions.append((node, element))
            else:
                negative_directions.append((node, element))

# Зануляем опорный элемент.
# Если есть ветка, в которой только источник ЭДС, то
# зануляем узел от которого он выходит и приравниваем к ЭДС узел в котрый он входит
# Если такого нет - зануляем первый узел из известных
if positive_directions:
    phi[positive_directions[0][0]] = 0
    negative_node = list(set(positive_directions[0][1].get_nodes()) - {positive_directions[0][0]})[0]
    phi[negative_node] = positive_directions[0][1].voltage
else:
    phi[list(nodes.keys())[0]] = 0
if len(list(set(positive_directions) | set(negative_directions))) > 2: # Два потому что 1 в + направлении и один в -
    # С двумя считать пока не умеем.
    raise ValueError('Источник тока без других элементов на ветке должен быть один на всю цепь!')
print(f'phi: {phi}')


sum_g = {}
sum_neightbours_g: dict[int, dict[int, list[float, float]]] = {}
sum_e = {} # TODO
sum_j = {}
# Пока только резистор, потом сделаем конденсатор
element_class = Resistor
for node, connected_nodes in circuit.find_nodes_with_element(element_class).items():
    if phi[node] != None:
        continue
    sum_neightbours_g[node] = {}
    g = 0
    for sub_node, elements in connected_nodes.items():
        elements = list(filter(lambda x: isinstance(x, element_class), elements))
        node_g = 0
        for element in elements:
            g += (1 / element.resistance)
            node_g += (1 / element.resistance)
        sum_neightbours_g[node][sub_node] = [node_g, -node_g, False]
        sum_e[node] = node_g # TODO
        if phi[sub_node] != None:
            sum_neightbours_g[node][sub_node][1] *= phi[sub_node]
            sum_neightbours_g[node][sub_node][2] = True
    sum_g[node] = g

element_class = ElectromotiveForce
for node, connected_nodes in circuit.find_nodes_with_element(element_class).items():
    if phi[node] != None:
        continue
    sum_e[node] = {}
    for sub_node, elements in connected_nodes.items():
        elements = list(filter(lambda x: isinstance(x, element_class), elements))
        sum_e[node][sub_node] = 0
        for element in elements:
            voltage = element.voltage
            element_direction = circuit.get_element_direction(node, element, element.node1)
            if element_direction:
                voltage = -voltage
            sum_e[node][sub_node] += voltage
        sum_e[node][sub_node] *= sum_neightbours_g[node][sub_node][0]
element_class = CurrentSource
for node, connected_nodes in circuit.find_nodes_with_element(element_class).items():
    if phi[node] != None:
        continue
    sum_j[node] = 0
    for sub_node, elements in connected_nodes.items():
        elements = list(filter(lambda x: isinstance(x, element_class), elements))
        for element in elements: # TODO: Вроде верно, надо будет проверить
            current = element.current
            element_direction = circuit.get_element_direction(node, element, element.node1)
            if element_direction:
                current = -current
            sum_j[node] += current

print(sum_g) # Сумма все проводимостей элементов, с которыми свзяан узел
print(sum_neightbours_g) # Сумма проводимостей на ветке между каждым узлом, с которым связан наш узел
print(sum_e) # Мб неверно. Сумма всех эдс, умноженых на проводимость, соединенных с узлом
print(sum_j) # Сумма всех источников тока, соединенных с узлом

lefts = [[0 for _ in range(len(circuit.get_graph().nodes))] for _ in range(len(circuit.get_graph().nodes))]
rights = [0 for _ in range(len(circuit.get_graph().nodes))]

for key, value in sum_j.items():
    rights[key-1] += value
for key, value in sum_e.items():
    for sub_value in value.values():
        rights[key-1] += sub_value
for key, value in sum_g.items():
    left = lefts[key-1]
    left[key-1] = value
    lefts[key-1] = left
for key, value in sum_neightbours_g.items():
    left = lefts[key-1]
    for sub_key, sub_value in value.items():
        if not sub_value[2]:
            lefts[key-1][sub_key-1] = sub_value[1]
        else:
            rights[key-1] -= sub_value[1]
print('lefts', lefts)
print('rights', rights)

m = []
v = []
not_listed = []
for id in range(len(lefts)):
    pre_m = []
    if not all(v == 0 for v in lefts[id]):
        for sub_id in range(len(lefts[id])):
            if sub_id+1 in list(phi.keys()):
                pre_m.append(lefts[id][sub_id])
        m.append(pre_m)
        v.append(rights[id])
print(m)
print(v)

M = numpy.array(m)
V = numpy.array(v)
print(numpy.linalg.lstsq(M, V, rcond=None)[0])
