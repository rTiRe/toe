from elements import Element, Wire, CurrentSource, ElectromotiveForce
from circuit import Circuit
import inspect

print('Приветствуем!')
print('Схему предстоит вводить ручками и постепенно :(')
print('Должен допилить.')

circuit = Circuit()

while True:
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
print()
mashes = circuit.get_mashes()
if len(mashes) == 0:
    print('Контура не были найдены.')
else:
    while True:
        print()
        print('Найдены контура:')
        for num, mash in enumerate(mashes):
            print(f'{num+1}. {mash}')
        print()
        print('Последовательность точек = направление тока в контуре')
        mashes_to_reverse = input('Если нужно поменять направление в контурах, введите их через запятую [q для продолжения]: ').replace(' ', '').split(',')
        if mashes_to_reverse[0] == 'q':
            break
        for mash in mashes_to_reverse:
            circuit.reverse_mash(int(mash)-1)

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
#
# СМОТРИМ НАПРАВЛЕНИЕ ElectromotiveForce ДЛЯ КАЖДОГО НАЙДЕНОГО,
# ТОЛЬКО ЕСЛИ ОН ОДИН В ВЕТКЕ
#
for node, connected_nodes in nodes.items():
    for sub_node, elements in connected_nodes.items():
        elements = list(filter(lambda x: not isinstance(x, Wire), elements))
        if len(elements) == 1 and isinstance(elements[0], ElectromotiveForce):
            element = elements[0]
            # print(node, sub_node, element.name)
            element_direction = circuit.get_element_direction(node, element, element.node1)
            print(node, element.name, element_direction)
