from abc import abstractmethod
from typing import Self


class Element:
    _elements: dict[tuple, Self] = {}

    @staticmethod
    def __new__(cls, point1: int, point2: int, *args) -> None:
        new_key = (int(point1), int(point2))
        if new_key not in Element._elements.keys():
            cls._elements[new_key] = super().__new__(cls)
        return cls._elements[new_key]
        

    @abstractmethod
    def __init__(self, point1: int, point2: int, name: str) -> None:
        self.__point1 = point1
        self.__point2 = point2
        #TODO: что если зададут уже указанные точки?
        self._name = name

    @property
    def point1(self) -> int:
        return self.__point1

    @point1.setter
    def point1(self, new_point) -> None:
        if not isinstance(new_point, (int, float, str)):
            raise TypeError('Точка должна быть int или типом, преобразуемым к int (float, str)')
        if new_point < 1:
            raise ValueError('Значение не может быть меньше 1!')
        self.__point1 = int(new_point)

    @property
    def point2(self) -> int:
        return self.__point2

    @point2.setter
    def point2(self, new_point) -> None:
        if not isinstance(new_point, (int, float, str)):
            raise TypeError('Точка должна быть int или типом, преобразуемым к int (float, str)')
        if new_point < 1:
            raise ValueError('Значение не может быть меньше 1!')
        self.__point2 = int(new_point)


class Resistor(Element):
    _global_name = 'Резистор'
    def __init__(self, point1: int, point2: int, name: str, resistance: float) -> None:
        super().__init__(point1, point2, f'R_{name}')
        self._resistance = resistance

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
    def __init__(self, point1: int, point2: int, name: str, voltage: float) -> None:
        super().__init__(point1, point2, f'J_{name}')
        self._voltage = voltage

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
    def __init__(self, point1: int, point2: int, name: str, current: float) -> None:
        super().__init__(point1, point2, f'I_{name}')
        self._current = current

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
    def __init__(self, point1: int, point2: int) -> None:
        super().__init__(point1, point2, 'Wire')