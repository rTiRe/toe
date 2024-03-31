from networkx import Graph, simple_cycles
from elements import Element

class Circuit:
    def __init__(self) -> None:
        self.__points = Graph()
        self.__elements = Element._elements
        self.__mashes = list() # Порядок точек контура = направление контурного тока.

    def add_element(self) -> None:
        points = list(self.__elements)[-1]
        self.__points.add_edge(points[0], points[1])
        self.find_mashes()

    def get_points(self) -> Graph:
        return self.__points.nodes

    def find_mashes(self) -> None:
        self.__mashes = list(simple_cycles(self.__points))

    def get_mashes(self) -> list:
        return self.__mashes