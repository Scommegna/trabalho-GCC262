from NodeModel import Node

#Graph Class
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

    def __repr__(self):
        return str(self.adj_list)


