import os
import sys
import streamlit as st
import plotly.graph_objects as go

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from src.graph_loader import load_graph, time_cost, distance_cost
from src.router import shortest_path, path_cost

# Page configuration
st.set_page_config(page_title="3D Route Planner Engine", layout="wide")
st.title("🌐 Intelligent Route Planner: 3D Network Visualization")
st.sidebar.header("Control Panel Matrices")

# Load graph data
csv_path = os.path.join(BASE_DIR, "data", "roads.csv")
if not os.path.exists(csv_path):
    st.error("Dataset matrix 'data/roads.csv' not found. Please run main.py first to generate it.")
    st.stop()

graph = load_graph(csv_path)

# Extract nodes and assign a pseudo-elevation (Z-axis) for 3D perspective
nodes_dict = {}
for u, v, data in graph.edges(data=True):
    # CRITICAL FIX: [1:] strips out the 'N' character from the string before casting to float
    nodes_dict[u] = {"lat": data["lat_u"], "lon": data["lon_u"], "elevation": float(u.split('_')[0][1:]) * 15.0}
    nodes_dict[v] = {"lat": data["lat_v"], "lon": data["lon_v"], "elevation": float(v.split('_')[0][1:]) * 15.0}

# Sidebar Selectors
all_nodes = sorted(list(graph.nodes))
src_node = st.sidebar.selectbox("Select Source Intersection", all_nodes, index=0)
dst_node = st.sidebar.selectbox("Select Target Destination", all_nodes, index=len(all_nodes)-1)
metric = st.sidebar.selectbox("Optimization Parameter Profile", ["time", "distance", "money", "eco"])

if src_node == dst_node:
    st.sidebar.error("Source and Destination cannot be identical.")
    st.stop()

# Compute optimal path using existing router module core
try:
    computed_path = shortest_path(graph, src_node, dst_node, objective=metric)
    calc_time = path_cost(graph, computed_path, time_cost)
    calc_dist = path_cost(graph, computed_path, distance_cost)
except Exception as e:
    st.error(f"Routing computation failure: {e}")
    st.stop()

# Display performance telemetry
col1, col2, col3 = st.columns(3)
col1.metric("Optimized Route Time", f"{round(calc_time, 2)} seconds")
col2.metric("Total Physical Distance", f"{round(calc_dist, 2)} meters")
col3.metric("Total Intersection Hops", f"{len(computed_path)} nodes")

# --- BUILD PLOTLY 3D GRAPH ---
fig = go.Figure()

# 1. Plot all network road infrastructure links (Edges)
edge_x, edge_y, edge_z = [], [], []
for u, v in graph.edges():
    edge_x.extend([nodes_dict[u]["lon"], nodes_dict[v]["lon"], None])
    edge_y.extend([nodes_dict[u]["lat"], nodes_dict[v]["lat"], None])
    edge_z.extend([nodes_dict[u]["elevation"], nodes_dict[v]["elevation"], None])

fig.add_trace(go.Scatter3d(
    x=edge_x, y=edge_y, z=edge_z,
    mode='lines',
    line=dict(color='#888888', width=3),
    name='Active Network Infrastructure',
    hoverinfo='none'
))

# 2. Plot all intersection points (Nodes)
node_x = [info["lon"] for info in nodes_dict.values()]
node_y = [info["lat"] for info in nodes_dict.values()]
node_z = [info["elevation"] for info in nodes_dict.values()]
node_text = list(nodes_dict.keys())

fig.add_trace(go.Scatter3d(
    x=node_x, y=node_y, z=node_z,
    mode='markers',
    marker=dict(size=6, color='#1f77b4', opacity=0.9),
    text=node_text,
    hoverinfo='text',
    name='Intersections'
))

# 3. Highlight the Active Computed Route Path
path_x = [nodes_dict[node]["lon"] for node in computed_path]
path_y = [nodes_dict[node]["lat"] for node in computed_path]
path_z = [nodes_dict[node]["elevation"] for node in computed_path]

fig.add_trace(go.Scatter3d(
    x=path_x, y=path_y, z=path_z,
    mode='markers+lines',
    line=dict(color='#FF4B4B', width=7),
    marker=dict(size=8, color='#FF4B4B'),
    text=computed_path,
    hoverinfo='text',
    name='Optimized Trajectory Path'
))

# Set 3D visual map parameters
fig.update_layout(
    height=750,
    margin=dict(l=0, r=0, b=0, t=0),
    scene=dict(
        xaxis=dict(title='Longitude Coordinate', backgroundcolor="rgb(20, 24, 30)", gridcolor="gray", showbackground=True),
        yaxis=dict(title='Latitude Coordinate', backgroundcolor="rgb(20, 24, 30)", gridcolor="gray", showbackground=True),
        zaxis=dict(title='Pseudo-Elevation (Z)', backgroundcolor="rgb(20, 24, 30)", gridcolor="gray", showbackground=True),
    ),
    legend=dict(yanchor="top", y=0.95, xanchor="left", x=0.05)
)

st.plotly_chart(fig, use_container_width=True)