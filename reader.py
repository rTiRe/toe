"""Module for read circuit file."""

import networkx as nx

import complexes


def get_complex_value(
    element_type: str,
    omega: float | complex,
    element_value: float | complex,
) -> complex:
    """Get value in complex presentation.

    Args:
        element_type (str): type of element.
        omega (float | complex): circuit omega value.
        element_value (float | complex): value for representate.

    Returns:
        complex: _description_
    """
    if element_type == 'Capacitor':
        return complexes.get_xc(omega, element_value)
    elif element_type == 'Inductor':
        return complexes.get_xl(omega, element_value)
    return complex(element_value)


def read_elements(filename: str, omega: float | complex) -> nx.Graph:
    """Read every element in the file.

    Args:
        filename (str): file name for read. Defaults to None.
        omega (float | complex): circuit omega value. Defaults to None.

    Returns:
        nx.Graph: readed and transformet circuit.
    """
    graph = nx.Graph()
    with open(filename, 'r') as circuit_file:
        circuit_file_lines = circuit_file.readlines()
    for line in circuit_file_lines:
        parts = line.strip().split()
        element_type = parts[0]
        defult_edge_data = {
            'u_of_edge': parts[1],
            'v_of_edge': parts[2],
            'u': parts[1],
            'v': parts[2],
            'type': element_type,
        }
        if element_type == 'Wire':
            graph.add_edge(**defult_edge_data)
        else:
            element_value = complex(parts[4])
            element_value = get_complex_value(
                element_type,
                omega,
                element_value,
            )
            graph.add_edge(
                **defult_edge_data,
                name=parts[3],
                value=element_value,
            )
    return graph


def run_read(filename: str = None, omega: float = None) -> nx.Graph:
    """Run reding process.

    Args:
        filename (str): default file name for read. Defaults to None.
        omega (float): default circuit omega value. Defaults to None.

    Returns:
        nx.Graph: readed and transformet circuit.
    """
    if filename:
        print(f'Enter the filename: {filename}')
    else:
        filename = input('Enter the filename: ')
    if omega:
        print(f'Omega value here: {omega}')
    else:
        omega = float(input('Omega value here: '))
    graph = read_elements(filename, omega)
    print(f'{graph} created successfully!')
    return graph
