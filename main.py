"""
Main function to start the application

Author: Lucas Scommegna
"""

from AuxFuncs import read_dat_to_graph, export_solution_to_dat, build_service_mapping, read_all_dat_files_to_graphs

from SolutionFuncs import constructive_algorithm_from_graph

from time import perf_counter

start_total = perf_counter()

solution_method = input("Select solution method. To generate solution for all data or one file: (all/one)")

if solution_method == "one":
    filepath = input("Type the filename: ")
    graph, input_data = read_dat_to_graph(filepath)

    routes, total_cost, clocks_used  = constructive_algorithm_from_graph(graph)

    service_mapping = build_service_mapping(input_data)

    end_total = perf_counter()

    total_clocks = int((end_total - start_total) * 1e6)

    export_solution_to_dat(filepath, routes, service_mapping, total_cost, total_clocks, clocks_used, graph)
else:
    graph_array = read_all_dat_files_to_graphs()

    for graph, input_data, filepath in graph_array:
        routes, total_cost, clocks_used = constructive_algorithm_from_graph(graph)
        service_mapping = build_service_mapping(input_data)

        end_total = perf_counter()

        total_clocks = int((end_total - start_total) * 1e6)

        export_solution_to_dat(filepath, routes, service_mapping, total_cost, total_clocks, clocks_used, graph)

