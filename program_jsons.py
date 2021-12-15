#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 10:39:48 2021

@author: dwwaweru
"""

import csv
import requests
import json 
from bs4 import BeautifulSoup
import networkx as nx
from networkx.readwrite import json_graph

"""
Scraping Amtrak Website and Saving to JSON
"""
#Scrapping amtrak website for routes

url = "https://www.amtrak.com/train-routes"
r = requests.get(url)


html_text = r.text
soup = BeautifulSoup(html_text, 'html.parser')


route_descript = "feature-overview-info__paragraphText"
allroute_descript = soup.find_all(class_=route_descript)

amtrak_routes = {}
for route in allroute_descript:
    route_name = route.h4.get_text()
    
    path = route.p.get_text().split(" - ")
    amtrak_routes[route_name] = path

#some stops are split by backslashes which need to be removed
for k,v in amtrak_routes.items():
    new_v = []
    for l in v:
        l = l.split("/")
        new_v = new_v + l
    amtrak_routes[k] = new_v


# amtrak_json = "/Users/dwwaweru/Desktop/UMich/Fall21/SI507/finalprj/amtrak-routes.json"
# amtrak_routes = json.loads(amtrak_json)

  
# Create json of amtrak dictionary 
# with open('amtrak-routes.json', 'w') as file:
#     json_string = json.dumps(amtrak_routes, default=lambda o: o.__dict__, sort_keys=True, indent=2)
#     file.write(json_string)

"""
Generating Graph of Amtrak Stations
"""

#Making Amtrak Directed Graph
#creating list of edges (route connections)
route_connections = []
station_set = set()
for route in amtrak_routes.keys():
    for station in amtrak_routes[route]:
        station = station.rstrip('\r\xa0')
        station_set.add(station)
    stops = amtrak_routes[route]
    c = 0
    for i in range(len(stops)-1):
        pair = (stops[c], stops[c+1])
        c += 1
        route_connections.append(pair)

#Draw Graph
TrainGraph = nx.Graph()
TrainGraph.add_edges_from(route_connections)
data = json_graph.adjacency_data(TrainGraph)

# Create json of amtrak graph 
with open('amtrak-graph.json', 'w') as file:
    json_string = json.dumps(data, indent=2)
    file.write(json_string)
