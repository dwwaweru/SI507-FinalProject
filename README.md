# SI507-FinalProject
Final project for SI507. This program uses a graph to find the shortest Amtrak train ride between two cities. In this instances, shortest route indicates the minimum number of stations and not the amount of time between the first and last stop.

## Packages
csv, requests, json, bs4 (BeautifulSoup), networkx, flask

## Interacting with Program
This program relies on the user answering a few prompts in a Flask app. The user is asked to answer a series of questions about where they would like to travel as well as where they would like to stay once they arrive at their final destination. They can also choose the maximum price point for their stay. Finally, the output of their stay is returned showing up to 5 options for hotel stays. Interacting with this program requires a key for the Google Nearby Places API.

## Graph
The graph used in this program is made from data scraped from the Amtrak Train Route homepage. For each major train route, the stations along the path were constructed into nodes. Edges were made by pairing each adjacent station within the list of route stops. The graph is directed since the order in which you can travel from one station to another should be preserved.

## Data Sources
