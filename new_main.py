"""Main file."""

from circuit_utils import calculate_circuit_data
from equation_utils import Equation
from graph_utils import simplify_graph
from node_potentials_utils import process_edf_branches
from reader import run_read

DEFAULT_OMEGA = 10000

filename = 'examples/circuit5'
graph = run_read(filename, DEFAULT_OMEGA)
simplified_graph = simplify_graph(graph)
calculated_graph = calculate_circuit_data(simplified_graph)
phi = process_edf_branches(calculated_graph)

equation = Equation(calculated_graph, phi)
equation.calculate_left_part()
equation.calculate_right_part()
equation_result = equation.calculate()

for key_number, key in enumerate(list(phi.keys())):
    if phi[key] is None:
        phi[key] = equation_result[key_number]
print(phi)
