"""
Main function to start the application

Author: Lucas Scommegna
"""

from AuxFuncs import create_graph_from_input, draw_graph

from GraphModel import Graph

graph = Graph()

graph = create_graph_from_input(graph)

# draw_graph(graph)

print("Total de vértices:", graph.get_total_of_vertexes())
print("Total de arestas:", graph.get_total_of_edges())
print("Total de arcos:", graph.get_total_of_arcs())
print("Vértices requeridos:", graph.get_quantity_of_required_vertexes())
print("Arestas requeridas:", graph.get_quantity_of_required_edges())
print("Arcos requeridos:", graph.get_quantity_of_required_arcs())
print("Order strength:", graph.get_order_strength())
print("Componentes conectados:", graph.get_list_of_connected_components())
print("Grau mínimo:", graph.get_vertex_min_degree())
print("Grau máximo:", graph.get_vertex_max_degree())
print("Centralidade de intermediação:", graph.betweenness_centrality())
print("Caminho médio:", graph.get_average_path_length())
print("Diâmetro do grafo:", graph.get_diameter())

