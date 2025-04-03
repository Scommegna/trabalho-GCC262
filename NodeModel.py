"""
Node model:
    {
        node_id: Int,
        connections: Connection Array
    }
"""
from ConnectionModel import Connection

class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.connections = []

    def add_connection(self, destiny, traversal_cost, demand, connection_type):
        connection = Connection(destiny, traversal_cost, demand, connection_type)
        self.connections.append(connection)

    def get_connections(self):
        return self.connections

    def __repr__(self):
        return f"Node({self.node_id}): {self.connections}"

