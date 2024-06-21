"""Calculators for elements with reactive resistance."""


def get_xc(omega: float, capacitance: float, only_real_part: bool = False) -> complex | int:
    """Calculate the reactive resistance value for capacitor.

    Args:
        omega (float): angle acceleration value.
        capacitance (float): energy capactiance value for capacitor
        only_real_part: flag for development

    Returns:
        complex | int: complex or real part of the reactive resistance
    """
    default_j = complex(0, 1)
    react_resistance = (1 / (omega * capacitance)) * default_j
    if only_real_part:
        return react_resistance.real
    return -react_resistance


def get_xl(omega: float, inductance: float, only_real_part: bool = False) -> complex | int:
    """Calculate the reactive resistance value for inductivity.

    Args:
        omega (float): angle acceleration value.
        inductance (float): inductive energy value for inductor
        only_real_part: flag for development

    Returns:
        complex | int: complex or real part of the reactive resistance
    """
    default_j = complex(0, 1)
    react_resistance = ((omega * inductance)) * default_j
    if only_real_part:
        return react_resistance.real
    return react_resistance
