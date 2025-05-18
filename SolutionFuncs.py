from collections import deque
from typing import List

# Supõe-se que as classes Graph, Node e Connection já estejam definidas conforme fornecido anteriormente.

# Função para encontrar o caminho mais curto entre dois nós (Dijkstra)
def dijkstra_shortest_path(graph, start, end):
    import heapq

    queue = [(0, start, [start])]
    visited = set()

    while queue:
        cost, node, path = heapq.heappop(queue)
        if node == end:
            return path

        if node in visited:
            continue
        visited.add(node)

        for conn in graph.adj_list[node].connections:
            if conn.destiny not in visited:
                heapq.heappush(queue, (cost + conn.traversal_cost, conn.destiny, path + [conn.destiny]))
    return None

# Função para calcular custo de um caminho
def calculate_path_cost(graph, path: List[int]) -> int:
    cost = 0
    for i in range(len(path) - 1):
        origin = path[i]
        dest = path[i + 1]
        for conn in graph.adj_list[origin].connections:
            if conn.destiny == dest:
                cost += conn.traversal_cost
                break
    return cost

# Algoritmo construtivo atualizado
def constructive_algorithm_from_graph(graph):
    depot = graph.depot
    capacity = graph.capacity
    required_services = {
        "N": {n: {"demand": 1, "served": False} for n in graph.required_nodes},
        "E": {
            frozenset((u, v)): {
                "from": u, "to": v,
                "demand": next(c.demand for c in graph.adj_list[u].connections if c.destiny == v and c.connection_type == "E"),
                "served": False
            }
            for u, v in graph.required_edges
        },
        "A": {
            (u, v): {
                "from": u, "to": v,
                "demand": next(c.demand for c in graph.adj_list[u].connections if c.destiny == v and c.connection_type == "A"),
                "served": False
            }
            for u, v in graph.required_arcs
        }
    }

    routes = []

    while any(not s["served"] for svc in required_services.values() for s in svc.values()):
        route = [depot]
        remaining_capacity = capacity
        last_node = depot

        while True:
            best_service = None
            best_path = None
            best_cost = float("inf")
            best_type = None

            for s_type, services in required_services.items():
                for sid, s in services.items():
                    if s["served"] or s["demand"] > remaining_capacity:
                        continue
                    target = s["from"] if s_type in ["E", "A"] else sid
                    path = dijkstra_shortest_path(graph, last_node, target)
                    if path:
                        cost = calculate_path_cost(graph, path)
                        if cost < best_cost:
                            best_cost = cost
                            best_service = sid
                            best_path = path
                            best_type = s_type

            if not best_service:
                break

            # Adiciona caminho até o serviço, evitando duplicata
            if best_path:
                for node in best_path[1:]:
                    if route[-1] != node:
                        route.append(node)
                last_node = route[-1]

            # Executa o serviço
            if best_type == "N":
                remaining_capacity -= 1
                required_services["N"][best_service]["served"] = True

            elif best_type == "E":
                u, v = tuple(best_service)
                next_node = v if last_node == u else u
                if route[-1] != next_node:
                    route.append(next_node)
                remaining_capacity -= required_services["E"][best_service]["demand"]
                required_services["E"][best_service]["served"] = True
                last_node = next_node

            elif best_type == "A":
                u, v = best_service
                if route[-1] != v:
                    route.append(v)
                remaining_capacity -= required_services["A"][best_service]["demand"]
                required_services["A"][best_service]["served"] = True
                last_node = v

        # Fecha a rota voltando ao depósito
        if last_node != depot:
            back_path = dijkstra_shortest_path(graph, last_node, depot)
            if back_path:
                for node in back_path[1:]:
                    if route[-1] != node:
                        route.append(node)

        if route == [depot]:
            break

        routes.append(route)

    return routes