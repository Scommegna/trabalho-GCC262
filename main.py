"""
Main function to start the application

Author: Lucas Scommegna
"""

from AuxFuncs import draw_graph, read_dat_to_graph, graph_stats_table

from GraphModel import Graph

graph = Graph()

filepath = input("Type the filename: ")
graph = read_dat_to_graph(filepath, graph)

draw_graph(graph)

df_stats = graph_stats_table(graph)
print(df_stats)
