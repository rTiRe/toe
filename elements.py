from abc import abstractmethod
from typing import Self


class Element:
    _elements: dict[set, Self] = {}

    @staticmethod
    def __new__(cls, node1: int, node2: int, *args) -> None:
        new_key = frozenset({cls.__node_checker(node1), cls.__node_checker(node2)})
        if len(new_key) == 1:
            raise ValueError('Номера точек не могут быть одинаковыми!')
        if new_key not in Element._elements.keys():
            cls._elements[new_key] = super(Element, cls).__new__(cls)
        else:
            print('К указаным точкам уже привязан элемент! Удалите его, прежде чем прикреплять новый!')
        return cls._elements[new_key]

    @abstractmethod
    def __init__(self, node1: int, node2: int, name: str) -> None:
        self.node1 = node1
        self.node2 = node2
        self._name = name

    @staticmethod
    def __node_checker(node) -> int:
        if not isinstance(node, (int, float, str)):
            raise TypeError('Точка должна быть int или типом, преобразуемым к int (float, str)')
        try:
            node = int(node)
        except ValueError:
            raise ValueError(f'Невозможно преобразовать {node} к int')
        if node < 1:
            raise ValueError('Значение не может быть меньше 1!')
        return node

    @property
    def node1(self) -> int:
        return self.__node1

    @node1.setter
    def node1(self, new_node) -> None:
        self.__node1 = self.__node_checker(new_node)

    @property
    def node2(self) -> int:
        return self.__node2

    @node2.setter
    def node2(self, new_node) -> None:
        self.__node2 = self.__node_checker(new_node)

    def get_nodes(self) -> tuple:
        return (self.__node1, self.__node2)

    @property
    def name(self) -> str:
        return self._name


class Resistor(Element):
    _global_name = 'Резистор'
    def __init__(self, node1: int, node2: int, name: str, resistance: float) -> None:
        super().__init__(node1, node2, f'R_{name}')
        self.resistance = resistance

    @property
    def resistance(self) -> float:
        return self._resistance

    @resistance.setter
    def resistance(self, new_resistance: float) -> None:
        if not isinstance(new_resistance, float):
            raise TypeError(f'Значение сопротивления должно быть float, а не {type(new_resistance).__name__}')
        if new_resistance <= 0:
            raise ValueError('Значение сопротивления должно быть больше нуля!')
        self._resistance = new_resistance


class ElectromotiveForce(Element): #TODO: направление источника
    _global_name = 'Источник ЭДС'
    def __init__(self, node1: int, node2: int, name: str, voltage: float) -> None:
        super().__init__(node1, node2, f'J_{name}')
        self.voltage = voltage

    @property
    def voltage(self) -> float:
        return self._voltage

    @voltage.setter
    def voltage(self, new_voltage: float) -> None:
        if not isinstance(new_voltage, float):
            raise TypeError(f'Значение ЭДС должно быть float, а не {type(new_voltage).__name__}')
        if new_voltage == 0:
            raise ValueError('Значение ЭДС не должно быть равно нулю!')
        self._voltage = new_voltage


class CurrentSource(Element): #TODO: направление источника
    _global_name = 'Источник тока'
    def __init__(self, node1: int, node2: int, name: str, current: float) -> None:
        super().__init__(node1, node2, f'I_{name}')
        self.current = current

    @property
    def current(self) -> float:
        return self._current

    @current.setter
    def current(self, new_current: float) -> None:
        if not isinstance(new_current, float):
            raise TypeError(f'Значение тока должно быть float, а не {type(new_current).__name__}')
        if new_current == 0:
            ValueError('Значение тока не должно быть равно нулю!')
        self._current = new_current


class Wire(Element):
    _global_name = 'Провод'
    def __init__(self, node1: int, node2: int) -> None:
        super().__init__(node1, node2, 'Wire')