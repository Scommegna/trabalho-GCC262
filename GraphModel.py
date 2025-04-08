"""
Graph Model:
{
    adj_list: Dict[int, Node],
    required_nodes: Set[int],
    required_edges: Set[frozenset[int]],
    required_arcs: List[Tuple[int, int]],
    depot: Optional[int],
    capacity: Optional[int],
}
"""
from collections import defaultdict, deque
from NodeModel import Node
from AuxFuncs import floyd_warshall, reconstruct_path
import math

class Graph:
    def __init__(self):
        self.adj_list = {}
        self.required_nodes = set()
        self.required_edges = set()
        self.required_arcs = []
        self.depot = None
        self.capacity = None

    def add_node(self, node_id):
        if node_id not in self.adj_list:
            self.adj_list[node_id] = Node(node_id)

    def add_connection(self, origin, destiny, traversal_cost, demand, connection_type, required=True):
        self.add_node(origin)
        self.add_node(destiny)

        connection_data = (origin, destiny, connection_type)

        if connection_type == "E":
            self.adj_list[origin].add_connection(destiny, traversal_cost, demand, connection_type)
            self.adj_list[destiny].add_connection(origin, traversal_cost, demand, connection_type)

            if required and demand > 0:
                self.required_edges.add(frozenset([origin, destiny]))

        elif connection_type == "A":
            self.adj_list[origin].add_connection(destiny, traversal_cost, demand, connection_type)

            if required and demand > 0:
                self.required_arcs.append((origin, destiny))

    def mark_required_node(self, node_id):
        self.required_nodes.add(node_id)
        self.add_node(node_id)

    def set_depot(self, depot_id):
        self.depot = depot_id
        self.add_node(depot_id)

    def set_capacity(self, capacity):
        self.capacity = capacity

    def get_total_of_vertexes(self):
        return len(self.adj_list)

    def get_total_of_edges(self):
        seen = set()
        for node in self.adj_list.values():
            for neighbor in node.connections:
                if neighbor.connection_type == "E":
                    seen.add(frozenset((node.node_id, neighbor.destiny)))
        return len(seen)

    def get_total_of_arcs(self):
        count = 0
        for node in self.adj_list.values():
            for neighbor in node.connections:
                if neighbor.connection_type == "A":
                    count += 1
        return count

    def get_quantity_of_required_vertexes(self):
        return len(self.required_nodes)

    def get_quantity_of_required_edges(self):
        return len(self.required_edges)

    def get_quantity_of_required_arcs(self):
        return len(self.required_arcs)

    def get_order_strength(self):
        total_edges = self.get_total_of_edges()
        total_arcs = self.get_total_of_arcs()
        total = total_edges + total_arcs
        return total_arcs / total if total > 0 else 0

    def get_list_of_connected_components(self):
        visited = set()
        components = []

        for node_id in self.adj_list:
            if node_id not in visited:
                comp = bfs_for_connected_components(node_id, self.adj_list, visited)
                components.append(comp)

        return components

    def get_vertex_min_degree(self):
        min_deg = float('inf')
        for node in self.adj_list.values():
            connected = set()
            for neighbor in node.connections:
                connected.add((neighbor.destiny, neighbor.connection_type))
            for other in self.adj_list.values():
                for neighbor in other.connections:
                    if neighbor.destiny == node.node_id:
                        connected.add((other.node_id, neighbor.connection_type))
            min_deg = min(min_deg, len(connected))
        return min_deg if self.adj_list else 0

    def get_vertex_max_degree(self):
        max_deg = 0
        for node in self.adj_list.values():
            connected = set()
            for neighbor in node.connections:
                connected.add((neighbor.destiny, neighbor.connection_type))
            for other in self.adj_list.values():
                for neighbor in other.connections:
                    if neighbor.destiny == node.node_id:
                        connected.add((other.node_id, neighbor.connection_type))
            max_deg = max(max_deg, len(connected))
        return max_deg

    def betweenness_centrality(self):
        dist, next_node_dict = floyd_warshall(self)
        centrality = defaultdict(int)
        nodes = list(self.adj_list)

        for u in nodes:
            for v in nodes:
                if u != v:
                    path = reconstruct_path(u, v, next_node_dict)
                    for node in path[1:-1]:
                        centrality[node] += 1

        return dict(centrality)

    def get_average_path_length(self):
        dist, _ = floyd_warshall(self)
        total = 0
        count = 0

        for u in self.adj_list:
            for v in self.adj_list:
                if u != v and dist[u][v] != math.inf:
                    total += dist[u][v]
                    count += 1

        return total / count if count else 0

    def get_diameter(self):
        dist, _ = floyd_warshall(self)
        dia = 0
        for u in self.adj_list:
            for v in self.adj_list:
                if u != v and dist[u][v] != math.inf:
                    dia = max(dia, dist[u][v])
        return dia

    def __repr__(self):
        return str(self.adj_list)


def bfs_for_connected_components(start_node, graph_nodes, visited_set):
    queue = deque([start_node])
    visited_set.add(start_node)
    component = []

    while queue:
        current = queue.popleft()
        component.append(current)
        for neighbor in graph_nodes[current].connections:
            if neighbor.destiny not in visited_set:
                visited_set.add(neighbor.destiny)
                queue.append(neighbor.destiny)

    return component



