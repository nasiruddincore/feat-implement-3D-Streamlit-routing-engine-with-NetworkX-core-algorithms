import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from src.graph_loader import load_graph, time_cost, distance_cost
from src.router import shortest_path, path_cost

def test_routing_optimization_invariants():
    csv_path = os.path.join(BASE_DIR, "data", "roads.csv")
    
    # Safety Check: If test runs standalone before main.py, force build data
    if not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0:
        from main import generate_synthetic_map_data
        generate_synthetic_map_data(csv_path)
        
    graph = load_graph(csv_path)
    src, dst = "N0_0", "N4_4"
    
    fastest_time_route = shortest_path(graph, src, dst, objective="time")
    shortest_distance_route = shortest_path(graph, src, dst, objective="distance")
    
    # Structural functional invariants metrics asset testing
    assert path_cost(graph, fastest_time_route, time_cost) <= path_cost(graph, shortest_distance_route, time_cost)
    assert path_cost(graph, shortest_distance_route, distance_cost) <= path_cost(graph, fastest_time_route, distance_cost)