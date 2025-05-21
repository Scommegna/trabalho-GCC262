import math

import os

from GraphModel import Graph

import pandas as pd

import matplotlib.pyplot as plt

pd.set_option('display.max_colwidth', None)
pd.set_option('display.width', 1000)

# Read .dat file to create graph
def read_dat_to_graph(filename):
    filepath = os.path.join("selected_instances", filename)

    graph = Graph()

    with open(filepath, 'r') as file:
        lines = file.readlines()

    section = None
    input_data = {
        "ReN": [],
        "ReE": [],
        "ReA": []
    }

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
            parts = line.split()
            if parts[0].startswith("N"):
                node_id = int(parts[0][1:])
                demand = int(parts[1])
                service_cost = int(parts[2])
                graph.mark_required_node(node_id)
                input_data["ReN"].append({
                    "ReN.": f"N{node_id}",
                    "DEMAND": demand,
                    "S. COST": service_cost
                })

        # Parse required edges
        elif section == "REE":
            parts = line.split()
            if parts[0].startswith("E"):
                from_n = int(parts[1])
                to_n = int(parts[2])
                t_cost = int(parts[3])
                demand = int(parts[4])
                s_cost = int(parts[5])
                graph.add_connection(from_n, to_n, t_cost, demand, connection_type="E", required=True)
                input_data["ReE"].append({
                    "From N.": from_n,
                    "To N.": to_n,
                    "T. COST": t_cost,
                    "DEMAND": demand,
                    "S. COST": s_cost
                })

        # Parse required arcs
        elif section == "REA":
            parts = line.split()
            if parts[0].startswith("A"):
                from_n = int(parts[1])
                to_n = int(parts[2])
                t_cost = int(parts[3])
                demand = int(parts[4])
                s_cost = int(parts[5])
                graph.add_connection(from_n, to_n, t_cost, demand, connection_type="A", required=True)
                input_data["ReA"].append({
                    "FROM N.": from_n,
                    "TO N.": to_n,
                    "T. COST": t_cost,
                    "DEMAND": demand,
                    "S. COST": s_cost
                })

    return graph, input_data

def read_all_dat_files_to_graphs():
    results = []

    folder = "selected_instances"
    for filepath in os.listdir(folder):
        if filepath.endswith(".dat"):
            graph, input_data = read_dat_to_graph(filepath)
            results.append((graph, input_data, filepath))

    return results


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



def build_service_mapping(input_data):
    mapping = {}

    for i, item in enumerate(input_data['ReN'], start=1):
        node = int(item['ReN.'][1:])
        mapping[('N', node)] = i

    for i, item in enumerate(input_data['ReE'], start=len(mapping)+1):
        u = int(item['From N.'])
        v = int(item['To N.'])
        mapping[('E', frozenset({u, v}))] = i

    for i, item in enumerate(input_data['ReA'], start=len(mapping)+1):
        u = int(item['FROM N.'])
        v = int(item['TO N.'])
        mapping[('A', (u, v))] = i

    return mapping


def export_solution_to_dat(input_name, routes, service_mapping, total_cost, clocks_alg_ref, clocks_sol_ref, graph):
    os.makedirs("solutions", exist_ok=True)
    output_path = os.path.join("solutions", f"sol-{input_name}")

    with open(output_path, "w") as f:
        f.write(f"{total_cost}\n")
        f.write(f"{len(routes)}\n")
        f.write(f"{clocks_alg_ref}\n")
        f.write(f"{clocks_sol_ref}\n")

        for route_id, route in enumerate(routes, start=1):
            demand = 0
            cost = 0
            visit_count = 0

            triplets = []
            triplets.append("(D 0,1,1)")
            visit_count += 1

            for i in range(1, len(route)):
                u = route[i - 1]
                v = route[i]
                cost += next((c.traversal_cost for c in graph.adj_list[u].connections if c.destiny == v), 0)

                if ('N', v) in service_mapping:
                    sid = service_mapping[('N', v)]
                    triplets.append(f"(S {sid},{v},{v})")
                    demand += 1
                    visit_count += 1

                edge_key = frozenset({u, v})
                if ('E', edge_key) in service_mapping:
                    sid = service_mapping[('E', edge_key)]
                    triplets.append(f"(S {sid},{u},{v})")
                    demand += 1
                    visit_count += 1

                arc_key = (u, v)
                if ('A', arc_key) in service_mapping:
                    sid = service_mapping[('A', arc_key)]
                    triplets.append(f"(S {sid},{u},{v})")
                    demand += 1
                    visit_count += 1

            triplets.append("(D 0,1,1)")
            visit_count += 1

            f.write(f" 0 1 {route_id} {demand} {cost}  {visit_count} {' '.join(triplets)}\n")









