from abc import abstractmethod, ABC

@ABC
class Element:
    __elements: dict[tuple, 'Element'] = dict()

    def __new__(cls, point1: int, point2: int, name: str) -> None:
        if (point1, point2) not in cls.__elements:
            cls.__elements[(point1, point2)] = name
        

    @abstractmethod
    def __init__(self, point1: int, point2: int, name: str) -> None:
        Element.__elements[(point1, point2)] = self
        #TODO: что если зададут уже указанные точки?
        self._name = name


class Resistor(Element):
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


class ElectromotiveForce(Element):
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

class CurrentSource(Element):
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
    def __init__(self, point1: int, point2: int) -> None:
        super().__init__(point1, point2, 'Wire')