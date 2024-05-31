def get_xC(omega: float, capacitance: float, only_real_part: bool = False) -> complex | int:
    """Calculator of the reactive resistance value for capacitor.

    Args:
        omega (float): angle acceleration value.
        capacitance (float): energy capactiance value for capacitor
        only_real_part: flag for development

    Returns:
        complex | int: complex or real part of the reactive resistance
    """
    DEFAULT_J = complex(0, 1)
    react_resistance = ((omega * capacitance)) * DEFAULT_J
    if only_real_part:
        return react_resistance.real
    return react_resistance


def get_xL(omega: float, inductance: float, only_real_part: bool = False) -> complex | int:
    """Calculator of the reactive resistance value for inductivity.

    Args:
        omega (float): angle acceleration value.
        inductance (float): inductive energy value for inductor
        only_real_part: flag for development

    Returns:
        complex | int: complex or real part of the reactive resistance
    """
    DEFAULT_J = complex(0, 1)
    react_resistance = ((omega * inductance)) * DEFAULT_J
    if only_real_part:
        return react_resistance.real
    return react_resistance


