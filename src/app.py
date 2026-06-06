import os
import sys
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# cspell:words multicriteria

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from src.graph_loader import load_graph, time_cost, distance_cost, money_cost
from src.router import shortest_path, path_cost
from src.multicriteria import route_weighted
from src.dynamics import apply_realtime_incident

app = FastAPI(title="Intelligent Route Planner Production API Engine")
G_ENGINE = load_graph()

class NavigationPayload(BaseModel):
    source_node: str = Field(..., description="Starting node string identifier", example="N0_0")
    destination_node: str = Field(..., description="Target node string identifier", example="N4_4")
    optimization_metric: str = Field("time", description="Cost metrics parameter evaluation context")
    alpha: float = 1.0
    beta: float = 0.5
    gamma: float = 2.0
    live_congestion_vectors: list[list[str]] = []

HTTP_ERROR_RESPONSES = {
    404: {"description": "Nodal components missing from matrix topology maps."},
    500: {"description": "Internal routing failure encounter metrics."}
}

@app.post("/api/v1/route/calculate", responses=HTTP_ERROR_RESPONSES)
def calculate_optimal_route(payload: NavigationPayload):
    if payload.source_node not in G_ENGINE or payload.destination_node not in G_ENGINE:
        raise HTTPException(status_code=404, detail="Requested topological nodal identifier variants missing inside map matrix.")
        
    working_graph = G_ENGINE
    if payload.live_congestion_vectors:
        working_graph = apply_realtime_incident(G_ENGINE, payload.live_congestion_vectors, structural_severity_multiplier=3.5)
        
    try:
        if payload.optimization_metric == "weighted":
            calculated_path = route_weighted(
                working_graph, payload.source_node, payload.destination_node,
                payload.alpha, payload.beta, payload.gamma
            )
        else:
            calculated_path = shortest_path(working_graph, payload.source_node, payload.destination_node, payload.optimization_metric)
            
        return {
            "status": "success",
            "computed_path_sequence": calculated_path,
            "metrics": {
                "total_time_seconds": round(path_cost(working_graph, calculated_path, time_cost), 2),
                "total_distance_meters": round(path_cost(working_graph, calculated_path, distance_cost), 2),
                "financial_toll_cost": round(path_cost(working_graph, calculated_path, money_cost), 2)
            }
        }
    except Exception as error_context:
        raise HTTPException(status_code=500, detail=str(error_context))