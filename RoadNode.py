# -*- coding: utf-8 -*-
'''
@Time    : 2023/6/20 9:52
@Author  : Ericyi
@File    : RoadNode.py

'''
# Assign road from_node and to_node to road network

import geopandas as gpd
import networkx as nx
from shapely.geometry import MultiLineString

# Load the road network Shapefile
road_network = gpd.read_file(r'E:\CityDNA\beijing_xiaoqu\raw_data\road\road_result_110100_merged2384.shp')

# Create an empty network graph
graph = nx.Graph()

# Iterate over each road segment
for index, road_segment in road_network.iterrows():
    # Get the individual parts of the road segment
    road_geometry = road_segment.geometry

    if isinstance(road_geometry, MultiLineString):
        # Handle MultiLineString geometries
        for line in road_geometry.geoms:
            start_point = line.coords[0]
            end_point = line.coords[-1]

            # Add edge to the network graph
            graph.add_edge(start_point, end_point)
    else:
        # Handle LineString geometries
        start_point = road_geometry.coords[0]
        end_point = road_geometry.coords[-1]

        # Add edge to the network graph
        graph.add_edge(start_point, end_point)

# Give a unique identifier to each node
node_id = 1
for node in graph.nodes:
    graph.nodes[node]['node_id'] = node_id
    node_id += 1

# Add the node identifiers back to the road network Shapefile
for index, road_segment in road_network.iterrows():
    road_geometry = road_segment.geometry

    if isinstance(road_geometry, MultiLineString):
        start_point = road_geometry.geoms[0].coords[0]
        end_point = road_geometry.geoms[-1].coords[-1]
    else:
        start_point = road_geometry.coords[0]
        end_point = road_geometry.coords[-1]

    road_network.at[index, 'start_node'] = graph.nodes[start_point]['node_id']
    road_network.at[index, 'end_node'] = graph.nodes[end_point]['node_id']

road_network['start_node'] = road_network['start_node'].astype(int)
road_network['end_node'] = road_network['end_node'].astype(int)

# Save the modified road network Shapefile
road_network.to_file(r'E:\CityDNA\beijing_xiaoqu\raw_data\road\road_node_110100_merged2384.shp')

