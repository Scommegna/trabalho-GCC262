"""
Graph Model:
{
    adj_list: DictionaryOfNodes
}
"""
from collections import defaultdict, deque

from NodeModel import Node

from AuxFuncs import floyd_warshall, reconstruct_path

import math

class Graph:
    def __init__(self):
        self.adj_list = {}

    def add_node(self, node_id):
        if node_id not in self.adj_list:
            self.adj_list[node_id] = Node(node_id)

    def add_connection(self, node_id, destiny, traversal_cost, demand, connection_type):
        self.add_node(node_id)
        self.add_node(destiny)

        if connection_type == "A":
            self.adj_list[node_id].add_connection(destiny, traversal_cost, demand, connection_type)
        elif connection_type == "E":
            self.adj_list[node_id].add_connection(destiny, traversal_cost, demand, connection_type)
            self.adj_list[destiny].add_connection(node_id, traversal_cost, demand, connection_type)

    def get_node(self, node_id):
        return self.adj_list.get(node_id)

    # Quantity of vertexes
    def get_total_of_vertexes(self):
        return len(self.adj_list)

    # Quantity of edges
    def get_total_of_edges(self):
        seen_edges = set()
        quantity = 0

        for node in self.adj_list.values():
            for neighbor in node.connections:
                if neighbor.connection_type == "E":
                    u, v = sorted([node.node_id, neighbor.destiny])
                    if (u, v) not in seen_edges:
                        seen_edges.add((u, v))
                        quantity += 1

        return quantity

    # Quantity of arcs
    def get_total_of_arcs(self):
        quantity = 0

        for node in self.adj_list.values():
            for neighbor in node.connections:
                if neighbor.connection_type == "A":
                    quantity += 1

        return quantity

    # Quantity of required vertexes
    def get_quantity_of_required_vertexes(self):
        required_vertexes = set()

        for node_id, node in self.adj_list.items():
            for neighbor in node.connections:
                if neighbor.demand > 0:
                    required_vertexes.add(node_id)
                    break

        return len(required_vertexes)

    # Quantity of required edges
    def get_quantity_of_required_edges(self):
        seen_edges = set()

        for node in self.adj_list.values():
            for neighbor in node.connections:
                if neighbor.demand > 0 and neighbor.connection_type == "E":
                    edge = frozenset({node.node_id, neighbor.destiny})
                    seen_edges.add((edge))

        return len(seen_edges)

    # Quantity of required arcs
    def get_quantity_of_required_arcs(self):
        quantity = 0

        for node in self.adj_list.values():
            for neighbor in node.connections:
                if neighbor.demand > 0 and neighbor.connection_type == "A":
                    quantity += 1

        return quantity

    """
        Order strength = total_of_arcs / (total_of_edges + total_of_arcs)
    """
    def get_order_strength(self):
        quantity_of_edges = self.get_total_of_edges()
        quantity_of_arcs = self.get_total_of_arcs()

        total = quantity_of_arcs + quantity_of_edges

        if total == 0:
            return 0

        return quantity_of_arcs / total

    # Get list of connected components
    def get_list_of_connected_components(self):
        visited_set = set()
        components_list = []

        for node_id in self.adj_list:
            if node_id not in visited_set:
                component = bfs_for_connected_components(node_id, self.adj_list, visited_set)
                components_list.append(component)

        return components_list

    # Get min degree of graph
    def get_vertex_min_degree(self):
        min_degree = float('inf')

        for node_id, node in self.adj_list.items():
            deg_set = set()
            deg = 0

            for neighbor in node.connections:
                if (neighbor.destiny, neighbor.connection_type) not in deg_set:
                    deg += 1
                    deg_set.add((neighbor.destiny, neighbor.connection_type))

            for other_node in self.adj_list.values():
                for neighbor in other_node.connections:
                    if neighbor.destiny == node_id:
                        if (other_node.node_id, neighbor.connection_type) not in deg_set:
                            deg += 1
                            deg_set.add((other_node.node_id, neighbor.connection_type))

            min_degree = min(min_degree, deg)

        if self.adj_list:
            return  min_degree

        return 0

    # Get max degree of graph
    def get_vertex_max_degree(self):
        max_degree = 0

        for node_id, node in self.adj_list.items():
            deg_set = set()
            deg = 0

            for neighbor in node.connections:
                if (neighbor.destiny, neighbor.connection_type) not in deg_set:
                    deg += 1
                    deg_set.add((neighbor.destiny, neighbor.connection_type))

            for other_node in self.adj_list.values():
                for neighbor in other_node.connections:
                    if neighbor.destiny == node_id:
                        if (other_node.node_id, neighbor.connection_type) not in deg_set:
                            deg += 1
                            deg_set.add((other_node.node_id, neighbor.connection_type))

            max_degree = max(max_degree, deg)

        return max_degree

    # Betweenness Centrality
    def betweenness_centrality(self):
        dist, next_node_dict = floyd_warshall(self)
        centrality = defaultdict(int)
        nodes = list(self.adj_list.keys())

        for u in nodes:
            for v in nodes:
                if u != v:
                    path = reconstruct_path(u, v, next_node_dict)

                    for node in path[1:-1]:
                        centrality[node] += 1

        return dict(centrality)

    # Average path length
    def get_average_path_length(self):
        dist, _ = floyd_warshall(self)
        total = 0
        count = 0

        for u in self.adj_list:
            for v in self.adj_list:
                if u != v and dist[u][v] != math.inf:
                    total += dist[u][v]
                    count += 1

        if count == 0:
            return count

        return total / count

    # Get graph diameter
    def get_diameter(self):
        dist, _ = floyd_warshall(self)
        diameter = 0

        for u in self.adj_list:
            for v in self.adj_list:
                if u != v and dist[u][v] != math.inf:
                    diameter = max(diameter, dist[u][v])

        return diameter

    def __repr__(self):
        return str(self.adj_list)


# BFS function to get connected components in a graph
def bfs_for_connected_components(start_node, graph_nodes, visited_set):
    component_list = []
    queue = deque([start_node])
    visited_set.add(start_node)

    while queue:
        current_node = queue.popleft()
        component_list.append(current_node)

        for neighbor in graph_nodes[current_node].connections:
            neighbor_id = neighbor.destiny

            if neighbor.connection_type == "E":
                if neighbor_id not in visited_set:
                    visited_set.add(neighbor_id)
                    queue.append(neighbor_id)

            elif neighbor.connection_type == "A":
                if neighbor_id not in visited_set:
                    visited_set.add(neighbor_id)
                    queue.append(neighbor_id)

    return component_list


