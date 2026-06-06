import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from src.graph_loader import load_graph, time_cost, distance_cost
from src.router import shortest_path, run_bfs, path_cost

def generate_synthetic_map_data(csv_path):
    """Constructs a clean 5x5 structural grid system layout to data/roads.csv."""
    import csv
    print(f"[INFO] Populating valid routing topology network map inside: {csv_path}")
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    
    rows = []
    node_id = lambda i, j: f"N{i}_{j}"
    coords = {node_id(i, j): (12.90 + i * 0.002, 77.50 + j * 0.002) for i in range(5) for j in range(5)}
    
    def add_edge_row(u_node, v_node, dist, speed, toll_val, direction, cls_type):
        rows.append([
            u_node, v_node, coords[u_node][0], coords[u_node][1], 
            coords[v_node][0], coords[v_node][1], dist, speed, toll_val, direction, cls_type
        ])
        
    for i in range(5):
        for j in range(5):
            if j + 1 < 5:
                add_edge_row(node_id(i, j), node_id(i, j + 1), 300, 40, 0, 0, "residential")
                add_edge_row(node_id(i, j + 1), node_id(i, j), 300, 40, 0, 0, "residential")
            if i + 1 < 5:
                add_edge_row(node_id(i, j), node_id(i + 1, j), 300, 35, 0, 0, "residential")
                add_edge_row(node_id(i + 1, j), node_id(i, j), 300, 35, 0, 0, "residential")
                
    with open(csv_path, "w", newline="", encoding="utf-8") as file_handler:
        writer = csv.writer(file_handler)
        writer.writerow("u,v,lat_u,lon_u,lat_v,lon_v,distance_m,speed_kph,toll,one_way,road_class".split(","))
        writer.writerows(rows)
    print("[SUCCESS] Foundational topography metrics file initialized successfully.")

def main():
    print("=" * 70)
    print("      INTELLIGENT ROUTE PLANNER PLATFORM ENGINE - CORE CLI INTERFACE   ")
    print("=" * 70)
    
    csv_path = os.path.join(BASE_DIR, "data", "roads.csv")
    
    # CRITICAL FIX: Regenerate if the data file is missing OR completely empty (0 bytes)
    if not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0:
        print("[WARN] Map grid missing or empty. Initializing foundational architecture...")
        generate_synthetic_map_data(csv_path)

    graph = load_graph(csv_path)
    print(f"[STATUS] Topography compiled: Found {len(graph.nodes)} nodes and {len(graph.edges)} active road segments.")
    
    if len(graph.nodes) == 0:
        print("[CRITICAL] Loaded graph matrix topology is empty! Terminating execution loop.")
        sys.exit(1)
        
    src_node, dst_node = "N0_0", "N4_4"
    print(f"\nProcessing Route Optimizations from Source '{src_node}' to Destination '{dst_node}':")
    print("-" * 70)
    
    # 1. Topological Intersections Hop Calculation (BFS)
    bfs_route = run_bfs(graph, src_node, dst_node)
    print(f"[*] BFS Structural Intersection Routing Track: {bfs_route}")
    
    # 2. Distance Minimized Evaluation
    shortest_dist_route = shortest_path(graph, src_node, dst_node, objective="distance")
    print(f"[+] Minimized Distance Footprint: {shortest_dist_route}")
    print(f"    - Net Track Distance: {path_cost(graph, shortest_dist_route, distance_cost)} meters")
    
    # 3. Spatial Heuristic Temporal Path Routing (A*)
    fastest_time_route = shortest_path(graph, src_node, dst_node, objective="time")
    print(f"[✓] Spatial A* Accelerated Temporal Path: {fastest_time_route}")
    print(f"    - Calculated Delay Window: {round(path_cost(graph, fastest_time_route, time_cost), 2)} seconds")
    print("=" * 70)

if __name__ == "__main__":
    main()