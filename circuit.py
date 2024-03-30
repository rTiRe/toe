from networkx import Graph, DiGraph, simple_cycles

from elements import Element, Resistor, ElectromotiveForce, CurrentSource, Wire

class Circuit:
    def __init__(self) -> None:
        self.__points = Graph()
        self.__elements = Element()

    def add_element(self) -> None:
        Resistor(1, 2, '1', 220)
        print(self.__elements.__elements)




# print(list(simple_cycles(Circuit)))