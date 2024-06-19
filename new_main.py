import numpy
import networkx as nx
from reader import run_read
from graph_utils import simplify_graph
from circuit_utils import calculate_circuit_data
from node_potentials_utils import process_edf_branches
from equation_utils import Equation

filename = 'examples/circuit2'
graph = run_read(filename, 10000)
simplified_graph = simplify_graph(graph)
calculated_graph = calculate_circuit_data(simplified_graph)
# for edge in calculated_graph.edges(data=True):
#     print(edge)
# for node in calculated_graph.nodes(data=True):
#     print(node)
phi = process_edf_branches(calculated_graph)

eq = Equation(calculated_graph, phi)
eq.calculate_left_part()
eq.calculate_right_part()
result = eq.calculate()

for id, key in enumerate(list(phi.keys())):
    if phi[key] == None:
        phi[key] = result[id]
print(phi)
