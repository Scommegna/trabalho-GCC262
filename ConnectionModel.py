"""
Connection model:
    {
        "destiny": NeighborId,
        "traversal_cost": Int,
        "demand": Int,
        "type": "A" | "E" (Arc or Edge)
    }
"""

class Connection:
    def __init__(self, destiny, traversal_cost, demand = 0, connection_type = 'E'):
        self.destiny = destiny
        self.traversal_cost = traversal_cost
        self.demand = demand
        self.connection_type = connection_type

    def __repr__(self):
        return f"{{'destiny': {self.destiny}, 'traversal_cost': {self.traversal_cost}, 'demand': {self.demand}, 'connection_type': {self.connection_type}}}"