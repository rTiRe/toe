from elements import Element
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
    element = elements[int(element_num) - 1]
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
    print('Найдены контура:')
    for num, mash in enumerate(mashes):
        print(f'{num+1}. {mash}')
print()
nodes = circuit.get_nodes()
if len(nodes) == 0:
    print('Узлы не были найдены.')
else:
    print('Найдены узлы:')
    for num, (node, connected_nodes) in enumerate(nodes.items()):
        print(f'{num+1}. {node}: {connected_nodes}')
print(circuit.get_element(2, 1).name, circuit.get_element(1, 2).get_nodes())
