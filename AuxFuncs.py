import math

import os

import pandas as pd

import matplotlib.pyplot as plt

pd.set_option('display.max_colwidth', None)
pd.set_option('display.width', 1000)

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
            parts = line.split()
            if parts[0].startswith("N"):
                node_id = int(parts[0][1:])
                graph.mark_required_node(node_id)
        elif section == "REE":
            parts = line.split()
            if parts[0].startswith("E"):
                u = int(parts[1])
                v = int(parts[2])
                cost = int(parts[3])
                demand = int(parts[4])
                graph.add_connection(u, v, cost, demand, connection_type="E", required=True)
        elif section == "REA":
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


def generate_solution_file(filename_input, routes, graph, total_cost, clocks_execucao=0, clocks_solucao=0):
    # Pasta de destino
    output_dir = "solutions"
    os.makedirs(output_dir, exist_ok=True)

    # Nome do arquivo de saída
    nome_base = os.path.splitext(os.path.basename(filename_input))[0]
    output_path = os.path.join(output_dir, f"sol-{nome_base}.dat")

    # Criar mapeamento de serviços com seus IDs
    service_map = {}
    service_id = 1

    # Nós requeridos
    for node in sorted(graph.required_nodes):
        service_map[('N', node)] = service_id
        service_id += 1

    # Arestas requeridas
    for edge in sorted(graph.required_edges, key=lambda x: (min(x), max(x))):
        u, v = sorted(edge)
        service_map[('E', u, v)] = service_id
        service_id += 1

    # Arcos requeridos
    for arc in sorted(graph.required_arcs):
        u, v = arc
        service_map[('A', u, v)] = service_id
        service_id += 1

    lines = []
    lines.append(f"{total_cost}")
    lines.append(f"{len(routes)}")
    lines.append(f"{clocks_execucao}")
    lines.append(f"{clocks_solucao}")

    # Utilizado para evitar múltiplos contadores por serviço
    visited_services = set()

    for idx, route in enumerate(routes):
        demand_total = 0
        custo_total = 0
        visitas = []

        for i in range(1, len(route)):
            u = int(route[i - 1])
            v = int(route[i])
            if i == 1:
                visitas.append("(D 0,1,1)")

            found = False

            # Verifica se é um serviço de nó
            if v in graph.required_nodes and (('N', v) not in visited_services):
                visitas.append(f"(S {service_map[('N', v)]},{v},{v})")
                visited_services.add(('N', v))
                # Procurar a demanda/custo
                for c in graph.adj_list[v].connections:
                    if c.destiny == v:
                        demand_total += c.demand
                        custo_total += c.traversal_cost
                        break

            # Verifica se é um serviço de aresta
            elif frozenset([u, v]) in graph.required_edges and (('E', min(u, v), max(u, v)) not in visited_services):
                visitas.append(f"(S {service_map[('E', min(u, v), max(u, v))]},{u},{v})")
                visited_services.add(('E', min(u, v), max(u, v)))
                for c in graph.adj_list[u].connections:
                    if c.destiny == v and c.connection_type == 'E':
                        demand_total += c.demand
                        custo_total += c.traversal_cost
                        break

            # Verifica se é um serviço de arco
            elif (u, v) in graph.required_arcs and (('A', u, v) not in visited_services):
                visitas.append(f"(S {service_map[('A', u, v)]},{u},{v})")
                visited_services.add(('A', u, v))
                for c in graph.adj_list[u].connections:
                    if c.destiny == v and c.connection_type == 'A':
                        demand_total += c.demand
                        custo_total += c.traversal_cost
                        break

        visitas.append("(D 0,1,1)")
        total_visitas = len(visitas)
        route_line = f" 0 1 {idx + 1} {demand_total} {custo_total}  {total_visitas} " + " ".join(visitas)
        lines.append(route_line)

    # Escrever no arquivo
    with open(output_path, 'w') as f:
        f.write("\n".join(lines))

    return output_path


