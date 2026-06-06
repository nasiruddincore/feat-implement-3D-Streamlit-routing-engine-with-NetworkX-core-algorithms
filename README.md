# 🌐 Intelligent Route Planner: 3D Graph Analytics Engine

An interactive 3D route optimization platform engineered with Python and NetworkX. Parses spatial topologies to execute core DSA graph algorithms, including BFS, Dijkstra, and heuristic Spatial A*. Deploys a FastAPI microservice backend and a Streamlit dashboard visualizing multi-criteria path trajectories via interactive Plotly 3D graphs.

---

## 🛠️ System Architecture & Data Flow

```text
+-------------------------------------------------------------------------+
|                          CSV Spatial Topology                           |
|                            (data/roads.csv)                             |
+------------------------------------+------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                       NetworkX Core Graph Engine                        |
|        (Parses 25 Nodes, 80 Edge Segments & Multi-Criteria Costs)       |
+------------------------------------+------------------------------------+
                                     |
                  +------------------+------------------+
                  |                                     |
                  v                                     v
+----------------------------------+  +-----------------------------------+
|     FastAPI Microservice Core    |  |     Streamlit 3D Dashboard        |
|  (/api/v1/route/calculate [POST])|  | (Interactive Plotly Trajectories) |
+----------------------------------+  +-----------------------------------+
