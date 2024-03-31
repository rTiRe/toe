from networkx import Graph, simple_cycles
from elements import Element

class Circuit:
    def __init__(self) -> None:
        self.__graph = Graph()
        self.__elements = Element._elements
        self.__mashes = list() # Порядок точек контура = направление контурного тока.
        self.__nodes = dict()

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
        for node in self.__graph.nodes:
            connected_nodes = list(self.__graph[node].keys())
            if len(connected_nodes) > 2:
                self.__nodes[node] = connected_nodes

    def get_mashes(self) -> list:
        self.__find_mashes()
        return self.__mashes

    def get_nodes(self) -> list:
        self.__find_nodes()
        return self.__nodes

    def get_element(self, node1: int, node2: int) -> Element:
        return self.__elements[frozenset({node1, node2})]