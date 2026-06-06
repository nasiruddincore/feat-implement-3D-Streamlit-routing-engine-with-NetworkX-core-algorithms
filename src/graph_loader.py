import csv
import os
import networkx as nx

def load_graph(csv_path=None):
    if csv_path is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        csv_path = os.path.join(base_dir, "data", "roads.csv")
        
    graph_instance = nx.DiGraph()
    with open(csv_path, newline="") as file_handler:
        reader = csv.DictReader(file_handler)
        for row in reader:
            u, v = row["u"], row["v"]
            attrs = {
                "lat_u": float(row["lat_u"]), "lon_u": float(row["lon_u"]),
                "lat_v": float(row["lat_v"]), "lon_v": float(row["lon_v"]),
                "distance_m": float(row["distance_m"]),
                "speed_kph": float(row["speed_kph"]),
                "toll": int(row["toll"]),
                "one_way": int(row["one_way"]),
                "road_class": row["road_class"],
                "traffic_factor": 1.0
            }
            attrs["base_sec"] = attrs["distance_m"] / (attrs["speed_kph"] * 1000.0 / 3600.0)
            graph_instance.add_edge(u, v, **attrs)
    return graph_instance

def time_cost(edge_attrs): 
    return edge_attrs["base_sec"] * edge_attrs.get("traffic_factor", 1.0)

def distance_cost(edge_attrs): 
    return edge_attrs["distance_m"]

def money_cost(edge_attrs): 
    return float(edge_attrs["toll"] * 25.0)

def eco_cost(edge_attrs): 
    class_modifier = 0.85 if edge_attrs["road_class"] == "primary" else 1.15
    return time_cost(edge_attrs) * class_modifier