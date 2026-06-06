import math
import networkx as nx
from src.graph_loader import time_cost, distance_cost, money_cost, eco_cost

# cspell:words dphi dlambda astar

def path_cost(graph_instance, path, cost_fn):
    return sum(cost_fn(graph_instance[u][v]) for u, v in zip(path[:-1], path[1:]))

def weight_factory(cost_fn):
    return lambda u, v, attrs: cost_fn(attrs)

def haversine_m(lat1, lon1, lat2, lon2):
    earth_radius = 6371000.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    haversine_value = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    return 2 * earth_radius * math.asin(math.sqrt(haversine_value))

def astar_heuristic(graph_instance, node_one, node_two):
    try:
        out_edge = next(iter(graph_instance.out_edges(node_one, data=True)))[2]
        lat1, lon1 = out_edge["lat_u"], out_edge["lon_u"]
        target_edge = next(iter(graph_instance.out_edges(node_two, data=True)))[2]
        lat2, lon2 = target_edge["lat_u"], target_edge["lon_u"]
        
        linear_dist = haversine_m(lat1, lon1, lat2, lon2)
        return linear_dist / (90.0 * 1000.0 / 3600.0)
    except (StopIteration, IndexError, KeyError):
        return 0.0

def shortest_path(graph_instance, src, dst, objective="time"):
    objective_map = {"time": time_cost, "distance": distance_cost, "money": money_cost, "eco": eco_cost}
    selected_cost_fn = objective_map.get(objective, time_cost)
    
    if objective == "time":
        return nx.astar_path(
            graph_instance, src, dst, 
            heuristic=lambda n1, n2: astar_heuristic(graph_instance, n1, n2), 
            weight=weight_factory(selected_cost_fn)
        )
    return nx.shortest_path(graph_instance, src, dst, weight=weight_factory(selected_cost_fn))

def run_bfs(graph_instance, src, dst):
    return nx.shortest_path(graph_instance, source=src, target=dst)