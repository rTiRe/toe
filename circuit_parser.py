from circuit import Circuit
from elements import Resistor, ElectromotiveForce, CurrentSource, Wire

elements_classes = {
    'Resistor': Resistor,
    'ElectromotiveForce': ElectromotiveForce,
    'CurrentSource': CurrentSource,
    'Wire': Wire,
}

def parser(file_path: str, circuit: Circuit) -> None:
    file = open(file_path, 'r', encoding='utf-8')
    rows = file.readlines()
    file.close()
    for row in rows:
        row = row.split(' ')
        elements_classes[row[0]](*row[1:])
        circuit.add_element()