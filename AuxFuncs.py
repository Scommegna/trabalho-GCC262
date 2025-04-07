import math

import os

import pandas as pd

import matplotlib.pyplot as plt

# Read .dat file to create graph
def read_dat_to_graph(filename, graph):
    filepath = os.path.join("selected_instances", filename)

    with open(filepath, 'r') as file:
        lines = file.readlines()

    section = None

    for line in lines:
        line = line.strip()

        if not line or line.startswith("Name") or line.startswith("Optimal value") or line.startswith("#Vehicles"):
            continue

        if line.startswith("Capacity:"):
            graph.set_capacity(int(line.split()[-1]))
        elif line.startswith("Depot Node:"):
            graph.set_depot(int(line.split()[-1]))
        elif line.startswith("#Nodes:"):
            total_nodes = int(line.split()[-1])
            for v in range(1, total_nodes + 1):
                graph.add_node(v)
        elif line.startswith("ReN."):
            section = "REN"
            continue
        elif line.startswith("ReE."):
            section = "REE"
            continue
        elif line.startswith("EDGE"):
            section = None
            continue
        elif line.startswith("ReA."):
            section = "REA"
            continue
        elif line.startswith("ARC"):
            section = None
            continue

        if section == "REN":
            # Example: N4	1	1
            parts = line.split()
            if parts[0].startswith("N"):
                node_id = int(parts[0][1:])
                graph.mark_required_node(node_id)
        elif section == "REE":
            # Example: E1	2	3	18	1	19
            parts = line.split()
            if parts[0].startswith("E"):
                u = int(parts[1])
                v = int(parts[2])
                cost = int(parts[3])
                demand = int(parts[4])
                graph.add_connection(u, v, cost, demand, connection_type="E", required=True)
        elif section == "REA":
            # Example: A1	1	2	13	1	14
            parts = line.split()
            if parts[0].startswith("A"):
                u = int(parts[1])
                v = int(parts[2])
                cost = int(parts[3])
                demand = int(parts[4])
                graph.add_connection(u, v, cost, demand, connection_type="A", required=True)

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
    nodes = list(graph.adj_list.keys())
    num_nodes = len(nodes)

    angle_step = 2 * math.pi / num_nodes
    positions = {
        node: (
            math.cos(i * angle_step),
            math.sin(i * angle_step)
        )
        for i, node in enumerate(nodes)
    }

    fig, ax = plt.subplots(figsize=(8, 8))

    for node_id, (x, y) in positions.items():
        ax.plot(x, y, 'o', color='lightgray', markersize=20)
        ax.text(x, y, str(node_id), fontsize=12, ha='center', va='center')

    for node in graph.adj_list.values():
        x1, y1 = positions[node.node_id]

        for neighbor in node.connections:
            x2, y2 = positions[neighbor.destiny]

            dx, dy = x2 - x1, y2 - y1
            arrowprops = dict(
                arrowstyle='->',
                color='blue' if neighbor.connection_type == 'A' else 'black',
                lw=1.5,
                shrinkA=15,
                shrinkB=15
            )

            if neighbor.connection_type == 'E':
                ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=arrowprops)
            else:
                ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=arrowprops)

            label_x = (x1 + x2) / 2
            label_y = (y1 + y2) / 2
            ax.text(
                label_x,
                label_y,
                f'{neighbor.traversal_cost}/{neighbor.demand}',
                fontsize=8,
                color='red'
            )

    ax.set_aspect('equal')
    ax.axis('off')
    plt.title("Graph Visualization:")
    plt.show()

# Create table of statistics
def graph_stats_table(graph):
    stats = {
        "Total de vértices": graph.get_total_of_vertexes(),
        "Total de arestas": graph.get_total_of_edges(),
        "Total de arcos": graph.get_total_of_arcs(),
        "Vértices requeridos": graph.get_quantity_of_required_vertexes(),
        "Arestas requeridas": graph.get_quantity_of_required_edges(),
        "Arcos requeridos": graph.get_quantity_of_required_arcs(),
        "Order strength": graph.get_order_strength(),
        "Componentes conectados": [graph.get_list_of_connected_components()],
        "Grau mínimo": graph.get_vertex_min_degree(),
        "Grau máximo": graph.get_vertex_max_degree(),
        "Centralidade de intermediação": [graph.betweenness_centrality()],
        "Caminho médio": graph.get_average_path_length(),
        "Diâmetro do grafo": graph.get_diameter()
    }

    df = pd.DataFrame.from_dict(stats, orient='index', columns=['Valor'])
    return df
