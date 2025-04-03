from GraphModel import Graph

def create_graph_from_input():
    graph = Graph()

    print("Type the type of input (list or matrix)")
    type_of_input = input().strip().lower()

    if type_of_input == "list":
        print("Type the list items in the following format:")
        print("origin destiny cost demand connection_type")
        print("Type 'END' to finish the reading process")

        while True:
            line = input().strip()

            if line.upper() == "END":
                break

            origin, destiny, cost, demand, connection_type = line.split()
            graph.add_connection(int(origin), int(destiny), int(cost), int(demand), connection_type.upper())