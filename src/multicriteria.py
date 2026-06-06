import networkx as nx
from src.graph_loader import time_cost, distance_cost, money_cost

# cspell:words candidate

def compound_cost(attrs, alpha=1.0, beta=0.5, gamma=2.0):
    return (alpha * time_cost(attrs)) + (beta * (distance_cost(attrs) / 1000.0)) + (gamma * money_cost(attrs))

def route_weighted(graph_instance, src, dst, alpha=1.0, beta=0.5, gamma=2.0):
    weight_calculator = lambda u, v, attrs: compound_cost(attrs, alpha, beta, gamma)
    return nx.shortest_path(graph_instance, src, dst, weight=weight_calculator)

def compute_pareto_front(graph_instance, src, dst, sample_depth=6):
    raw_paths = list(nx.shortest_simple_paths(graph_instance, src, dst, weight=lambda u, v, a: time_cost(a)))[:sample_depth]
    scored_profiles = []
    
    for current_path in raw_paths:
        t_sum = sum(time_cost(graph_instance[u][v]) for u, v in zip(current_path[:-1], current_path[1:]))
        d_sum = sum(distance_cost(graph_instance[u][v]) for u, v in zip(current_path[:-1], current_path[1:]))
        m_sum = sum(money_cost(graph_instance[u][v]) for u, v in zip(current_path[:-1], current_path[1:]))
        scored_profiles.append((current_path, (t_sum, d_sum, m_sum)))
        
    pareto_optimal_set = []
    for candidate_path, candidate_vector in scored_profiles:
        is_dominated = False
        for _, competitor_vector in scored_profiles:
            if all(comp <= candidate for comp, candidate in zip(competitor_vector, candidate_vector)) and \
               any(comp < candidate for comp, candidate in zip(competitor_vector, candidate_vector)):
                is_dominated = True
                break
        if not is_dominated and (candidate_path, candidate_vector) not in pareto_optimal_set:
            pareto_optimal_set.append((candidate_path, candidate_vector))
            
    return pareto_optimal_set