import math

import networkx as nx
import matplotlib.pyplot as plt

# Read input data and creates graph
def create_graph_from_input(graph):
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

    elif type_of_input == "matrix":
        print("Type the data matrix")
        print("Type the data in the following format: cost, demand, type or 0 if it does not has connection.")
        print("Example: 0 5,7,E 20,5,A 0")
        print("Type 'END' to finish the reading process")

        matrix = []

        while True:
            line = input().strip()

            if line.upper() == "END":
                break

            matrix.append(line.split())

        n = len(matrix)
        for i in range(n):
            for j in range(len(matrix[i])):
                value = matrix[i][j]

                if value != "0":
                    data = value.split(",")
                    cost = int(data[0])
                    demand = int(data[1])
                    connection_type = data[2].upper()

                    graph.add_connection(i, j, cost, demand, connection_type)
    else:
        print("Invalid input.")
        return None

    return graph

# Floyd-Warshall algorithm
def floyd_warshall(graph):
    dist = {}
    next_node_dict = {}
    vertexes = list(graph.adj_list.keys())

    for u in vertexes:
        dist[u] = {}
        next_node_dict[u] = {}

        for v in vertexes:
            dist[u][v] = math.inf
            next_node_dict[u][v] = None

        dist[u][u] = 0

    for u in graph.adj_list:
        for neighbor in graph.adj_list[u].connections:
            v = neighbor.destiny
            cost = neighbor.traversal_cost
            dist[u][v] = cost
            next_node_dict[u][v] = v

    for k in vertexes:
        for i in vertexes:
            for j in vertexes:
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    next_node_dict[i][j] = next_node_dict[i][k]

    return dist, next_node_dict

def reconstruct_path(u, v, next_node):
    if next_node[u][v] is None:
        return []

    path = [u]

    while u != v:
        u = next_node[u][v]
        path.append(u)

    return path

# Plot Graph
def draw_graph(graph):
    G = nx.DiGraph()

    for node in graph.adj_list.values():
        for neighbor in node.connections:
            G.add_edge(
                node.node_id,
                neighbor.destiny,
                label=f'{neighbor.traversal_cost}/{neighbor.demand}',
                color='blue' if neighbor.connection_type == "A" else 'black'
            )

    position = nx.spring_layout(G)
    edge_labels = nx.get_edge_attributes(G, 'label')
    edge_colors = [G[u][v]['color'] for u, v in G.edges]

    nx.draw(G, position, with_labels=True, edge_color=edge_colors, node_size=700, node_color='lightgray')
    nx.draw_networkx_edge_labels(G, position, edge_labels=edge_labels)
    plt.title("Visualização do Grafo")
    plt.show()
