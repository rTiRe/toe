from networkx import Graph, simple_cycles
from elements import Element, Wire, Resistor
from copy import deepcopy

class Circuit:
    def __init__(self) -> None:
        self.__graph = Graph()
        self.__elements = Element._elements
        self.__mashes = list() # Порядок точек контура = направление контурного тока.
        self.__nodes = dict()

    def get_graph(self) -> Graph:
        return self.__graph

    def add_element(self) -> None:
        points = list(self.__elements)[-1]
        self.__graph.add_edge(*points)

    def get_points(self) -> Graph:
        return self.__graph.nodes

    def __find_mashes(self) -> None:
        raw_mashes = list(simple_cycles(self.__graph))
        if not raw_mashes:
            return
        self.__mashes.append(tuple(max(raw_mashes, key=len)))
        for first_mash in raw_mashes:
            append = True
            for second_mash in raw_mashes:
                if first_mash is second_mash:
                    continue
                if set(second_mash).issubset(first_mash):
                    append = False
                    break
            if append:
                self.__mashes.append(tuple(first_mash))
        self.__mashes = list(set(self.__mashes))

    def __find_nodes(self) -> None:
        raw_nodes: dict[dict] = dict()
        for node in self.__graph.nodes:
            connected_nodes = list(self.__graph[node].keys())
            if len(connected_nodes) > 2:
                raw_nodes[node] = connected_nodes
        # print(raw_nodes)
        for node, nodes in raw_nodes.items():
            sub_nodes = dict()
            for sub_node in nodes:
                is_node = False
                elements = [self.get_element(node, sub_node)]
                prev_node = node
                # перебираем все исходящие друг из друга точки пока не найдем узел
                while not is_node:
                    if sub_node in raw_nodes.keys():
                        break
                    node_elements = self.get_elements(sub_node)
                    this_element = self.get_element(prev_node, sub_node)
                    next_element = list(set(node_elements) - set([this_element]))[0]
                    # print(next_element.get_nodes())
                    elements.append(next_element)
                    # deepcopy чтобы при изменении sub_node не менялось prev_node
                    # prev_node - предыдущая нода
                    prev_node = deepcopy(sub_node)
                    sub_node: int = list(next_element.get_nodes() - {sub_node})[0]
                # Сохраняем только кратчайший путь
                if sub_node in sub_nodes and len(elements) > len(sub_nodes[sub_node]):
                    continue
                sub_nodes[sub_node] = tuple(elements)
            self.__nodes[node] = sub_nodes

    def get_mashes(self) -> list:
        self.__find_mashes()
        return self.__mashes

    def reverse_mash(self, mash_index: int) -> None:
        mash = self.__mashes[mash_index]
        self.__mashes[mash_index] = tuple(reversed(mash))

    def get_nodes(self) -> dict:
        self.__find_nodes()
        return self.__nodes

    def get_element(self, node1: int, node2: int) -> Element:
        return self.__elements[frozenset({node1, node2})]

    def get_elements(self, node: int) -> tuple[Element]:
        elements = []
        for key in self.__elements.keys():
            if node in key:
                elements.append(self.__elements[frozenset({node, list(key - {node})[0]})])
        return tuple(elements)

    def get_element_direction(self, main_node: int, element: Element, element_node: int) -> bool | None:
        """True если направлено от main_node"""
        if len(self.__nodes) < 2:
            return
        if main_node not in self.__nodes.keys():
            raise ValueError('Указанная основная точка - не узел!')
        if isinstance(element, (Wire, Resistor)):
            raise TypeError('Данный элемент не имеет направления!')
        element_nodes = element.get_nodes()
        if element_node not in element_nodes:
            raise ValueError('Указанная точка не принадлежит данному элементу')
        while True:
            if element_node in list(self.__nodes):
                if element_node == main_node:
                    return True
                return False
            # print(element_node, self.get_elements(element_node))
            element: Element = list(set(self.get_elements(element_node)) - {element})[0]
            element_node = list(set(element.get_nodes()) - {element_node})[0]

    def find_nodes_with_element(self, element_class: type) -> dict[int, dict[int, tuple[Element]]]:
        nodes = dict()
        if not issubclass(element_class, Element):
            raise TypeError(f'{type(element_class).__name__} не Element!')
        if not  isinstance(element_class, type):
            raise TypeError(f'{element_class} не класс!')
        for node, connected_nodes in self.get_nodes().items():
            sub_nodes = dict()
            for sub_node, elements in connected_nodes.items():
                if any(isinstance(element, element_class) for element in elements):
                    sub_nodes[sub_node] = elements
            nodes[node] = sub_nodes
        return nodes
