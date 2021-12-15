# SI507-FinalProject
Final project for SI507. This program uses a graph to find the shortest Amtrak train ride between two cities. In this instances, shortest route indicates the minimum number of stations and not the amount of time between the first and last stop.

##Packages
csv, requests, json, bs4 (BeautifulSoup), networkx, flask

##Graph
The graph used in this program is made from data scrapped from the Amtrak Train Route homepage. For each major train route (ex. Acela), the stations along the path were constructed into edges. The graph is directed since the order in which you can travel from one station to another should be preserved.

##Data Sources
