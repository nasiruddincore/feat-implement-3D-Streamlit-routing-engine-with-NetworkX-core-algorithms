import networkx as nx

def apply_realtime_incident(graph_instance, incident_edge_list, structural_severity_multiplier=3.0):
    modified_graph = graph_instance.copy()
    for edge in incident_edge_list:
        if len(edge) == 2 and modified_graph.has_edge(edge[0], edge[1]):
            modified_graph[edge[0]][edge[1]]["traffic_factor"] = float(structural_severity_multiplier)
    return modified_graph

def remove_realtime_incident(graph_instance, incident_edge_list):
    modified_graph = graph_instance.copy()
    for edge in incident_edge_list:
        if len(edge) == 2 and modified_graph.has_edge(edge[0], edge[1]):
            modified_graph[edge[0]][edge[1]]["traffic_factor"] = 1.0
    return modified_graph