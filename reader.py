import networkx as nx
import complexes

def get_element_value(element_type, omega, value):
    if element_type == 'Capacitor':
        return complexes.get_xC(omega, value)
    elif element_type == 'Inductor':
        return complexes.get_xL(omega, value)
    return complex(value)

def read_elements(filename, omega):
    graph = nx.Graph()
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split()
            element_type = parts[0]
            node1, node2 = parts[1], parts[2]
            defult_edge_data = {
                'u_of_edge': node1,
                'v_of_edge': node2,
                'u': node1,
                'v': node2,
                'type': element_type,
            }
            if element_type != 'Wire':
                element_name, element_value = parts[3], complex(parts[4])
                element_value = get_element_value(element_type, omega, element_value)
                graph.add_edge(**defult_edge_data, name=element_name, value=element_value)
            else:
                graph.add_edge(**defult_edge_data)
    return graph

def run_read(filename: str = None, omega: float = None) -> nx.Graph:
    if filename:
        print(f'Enter the filename: {filename}')
    else:
        filename = input('Enter the filename: ')
    try:
        if omega:
            print(f'Omega value here: {omega}')
        else:
            omega = float(input('Omega value here: '))
        graph = read_elements(filename, omega)
        print(f'{graph} created successfully!')
        return graph
    except Exception as e:
        print(f'An error occurred: {e}')

if __name__ == '__main__':
    run_read()