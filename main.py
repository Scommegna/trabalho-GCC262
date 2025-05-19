"""
Main function to start the application

Author: Lucas Scommegna
"""

from AuxFuncs import draw_graph, read_dat_to_graph, graph_stats_table, export_solution_to_dat, build_service_mapping

from GraphModel import Graph

from SolutionFuncs import constructive_algorithm_from_graph

from time import perf_counter

start_total = perf_counter()
graph = Graph()

filepath = input("Type the filename: ")
graph, input_data = read_dat_to_graph(filepath, graph)

# draw_graph(graph)

# df_stats = graph_stats_table(graph)

routes, total_cost, clocks_used  = constructive_algorithm_from_graph(graph)

service_mapping = build_service_mapping(graph, input_data)

end_total = perf_counter()

total_clocks = int((end_total - start_total) * 1e6)

export_solution_to_dat(filepath, routes, service_mapping, total_cost, total_clocks, clocks_used, graph)


# print(df_stats)
