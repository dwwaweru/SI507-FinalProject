#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 20:04:33 2021

@author: dwwaweru
"""
import csv
import requests
import json 
from bs4 import BeautifulSoup
import networkx as nx
from flask import Flask, render_template, request


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

amtrak_stops = []
for route in amtrak_routes.values():
    for stop in route:
        amtrak_stops.append(stop)

# amtrak_json = "/Users/dwwaweru/Desktop/UMich/Fall21/SI507/finalprj/amtrak-routes.json"
# amtrak_routes = json.loads(amtrak_json)

  
# Create json of amtrak dictionary 
# json_object = json.dumps(amtrak_routes, indent = 3) 
#print(json_object)
#json.dump(amtrak_routes, open('amtrak-routes.json', "w"), indent=2)


#read in the station data
input_file = csv.DictReader(open("amtrak.csv"))
dict_list = []
for row in input_file:
    dict_list.append(row)
    
#keep only dictionaries of rail stations
rail_dicts = []
for i in range(len(dict_list)):
    if dict_list[i]["STNTYPE"] == "RAIL":
        rail_dicts.append(dict_list[i])


class doubleQuoteDict(dict):
    '''
    This function takes in the a dictionary and returns its keys with double
    quotes. This is necessary because HTML splits names with spaces so station
    names won't be searchable otherwise.'

    Parameters
    ----------
    a_dict: dicitonary we would like to convert

    Returns
    -------
    json string of input dicionary

    '''
    
    def __str__(self):
        return json.dumps(self)

    def __repr__(self):
        return json.dumps(self)


#Dictionary of Station Names
#key = station name; city, state
#val = id
station_names = {}
for i in range(len(rail_dicts)):
    if rail_dicts[i]["STNNAME"] in station_names.keys():
        key = rail_dicts[i]["STNNAME"]
        val_id = rail_dicts[i]["OBJECTID"]
        if rail_dicts[i]['CITY'] in amtrak_stops:
            station_names[key].append(val_id)
    else:
        key = rail_dicts[i]["STNNAME"]
        val_id = rail_dicts[i]["OBJECTID"]
        if rail_dicts[i]['CITY'] in amtrak_stops:
            station_names[key] = []
            station_names[key].append(val_id)


station_double = doubleQuoteDict(station_names)

#Dictionary of Cities with Station
#used to access the name of the input city to search graph
#key = station id
#val = station_city
station_cities = {}
for i in range(len(rail_dicts)):
    if rail_dicts[i]['OBJECTID'] in station_names.keys():
        key = rail_dicts[i]['OBJECTID']
        val_city = rail_dicts[i]['CITY']
        if val_city in amtrak_stops:
            station_cities[key].append(val_city)
    else:
        key = rail_dicts[i]['OBJECTID']
        val_city = rail_dicts[i]['CITY']
        if val_city in amtrak_stops:
            station_cities[key] = []
            station_cities[key].append(val_city)

cities_double = doubleQuoteDict(station_cities)


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


def shortest_path(graph, source, target):
    '''
    This function takes in a graph, a starting location and ending location
    and returns the shortest path between these cities.

    Parameters
    ----------
    graph: graph of Amtrak stations
    source: str of starting city name
    target: str of ending city name

    Returns
    -------
    path: list of city names representing the shortest path

    '''
    
    path = nx.shortest_path(TrainGraph, source, target)
    return path

def getstationinfo(city):
    '''
    This function takes in name of a city and returns a dictionary containing
    information about a station's location, name, address, and more.'
    
    Parameters
    ----------
    city = str of city name we will use to search dictionary of Amtrak stations

    Returns
    -------
    Dictionary of input city

    '''
    for i in range(len(rail_dicts)):
        if rail_dicts[i]['CITY'] == city:
            return rail_dicts[i]


def searchhotels(station_pt, price, proximity):
    '''
    This function calls the Google Nearby Search API and returns a list of 
    hotels matching the search criteria.

    Parameters
    ----------
    station_pt: tuple of the longitude and latitude of the destination train station
    price: string corresponding to the maximum amount of money the user will spend at a hotel
    proximity: str of the mile radius away from the station hotels should be searched for

    Returns
    -------
    hotel_list: list of Hotel class objects from search results

    '''
    #x=long, y=lat
    long = station_pt[0]
    lat = station_pt[1]
    key = "key=AIzaSyBsgFjCAccIUo8vQeWdpmkMJM_yU_9V7Ug"
    #assign price to numerical value
    if price == "an inexpensive":
        cost = 1
    elif price == "a moderate":
        cost = 2
    elif price == "an expensive":
        cost = 3
    else:
        cost = 4
    
    if proximity == "5":
        dist_m = 8065
    elif proximity == "10":
        dist_m = 1613
    else:
        dist_m = 40323
    
    base = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
    location = "location="+lat+'%2C'+long+"&"
    place = "type=lodging&"
    proximity = "radius="+str(dist_m)+"&"
    price = "maxprice="+str(cost)+"&"
    
    url = base+location+proximity+place+price+key


    payload={}
    headers = {}
    
    response = requests.request("GET", url, headers=headers, data=payload)
    hotel_output = json.loads(response.text) #list of results
    
    
    hotel_dict = {}
    hotel_dict['results'] = hotel_output
    
    
    
    class Hotel:
        def __init__(self, name, price, rating, address):
            self.name = name
            self.price = price
            self.rating = rating
            self.address = address
        
        #formatted output for initial search
        def searchinfo(self):
            '''
            assigns search info method to each class object
        
            Parameters
            ----------
            self = Hotel class object
            
            Returns
            -------
            Readable string of hotel cost, rating, and address
            '''
            if self.price == 0:
                cost = "free"
            elif self.price == 1:
                cost = "inexpensive"
            elif self.price == 2:
                cost = "moderately expensive"
            elif self.price == 3:
                cost = "expensive"
            else:
                cost = "very expensive"
            return(f"{self.name} is {cost}, rated {self.rating}/5, and can be found at:\n {self.address}")
        
    
    list_results = hotel_dict['results']['results']
    print(list_results)
    hotel_list = []
    if len(list_results) < 5:
        for i in range(len(list_results)):
            name = list_results[i]['name']
            price = list_results[i]['price_level']
            rating = list_results[i]['rating']
            address = list_results[i]['vicinity']
            h = Hotel(name, price, rating, address)
            hotel_list.append(h)
    else:  
        for i in range(len(list_results[:5])):
            name = list_results[i]['name']
            price = list_results[i]['price_level']
            rating = list_results[i]['rating']
            address = list_results[i]['vicinity']
            h = Hotel(name, price, rating, address)
            hotel_list.append(h)

    return hotel_list #returns list of hotel objects
 

app = Flask(__name__)

@app.route('/')
def index():
    city_li = station_double
    return render_template('FlaskInputs.html', cities=city_li) # just the static HTML
    

@app.route('/handle_form', methods=['POST'])
def handle_the_form():
    username = request.form["name"]
    start = request.form["origin"].strip(",")
    end = request.form["destination"].strip(",")
    expense = request.form["hotel_price"]
    radius = request.form["distance"]
    station_pt = (getstationinfo(end)["X"],getstationinfo(end)["Y"])
    hotel_li = searchhotels(station_pt,expense,radius)     
    path = [s for s in nx.shortest_path(TrainGraph, source=start, target=end)]
    num_hotel = len(hotel_li)
    #path = formatpath(path)
    return render_template('response.html',
        #response_val = var
        name=username,
        origin=start, 
        destination=end,
        hotel_price = expense,
        distance=radius,
        hotel_outputs = hotel_li,
        station_info = station_pt,
        short_path = path,
        n_hotel =num_hotel)
  
    
if __name__=="__main__":
    app.run(debug=True) 
    
    