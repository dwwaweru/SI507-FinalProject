# SI507-FinalProject
Final project for SI507. This program uses a graph to find the shortest Amtrak train ride between two cities. In this instance, the shortest route is based on passing through the minimum number of stations and not the amount of time between the first and last stop.

## Packages
csv, requests, json, bs4 (BeautifulSoup), networkx, flask

## Interacting with Program
This program relies on the user answering a few prompts in a Flask app. The user is asked to answer a series of questions about where they would like to travel as well as where they would like to stay once they arrive at their final destination. They can also choose the maximum price point for their stay. Finally, the output of their stay is returned showing up to 5 options for hotel stays. Interacting with this program requires a key for the Google Nearby Places API.

## Graph
The graph used in this program is made from data scraped from the Amtrak Train Route homepage. For each major train route, the stations along the path were constructed into nodes. Edges were made by pairing each adjacent station within the list of route stops. The graph is directed since the order in which you can travel from one station to another should be preserved.

## Data Sources
### Amtrak Route Information (HTML)
*Origin*. 
Website information scrapped from https://www.amtrak.com/train-routes
*Data Access*  
These data were accessed using BeautifulSoup to scrape the website. The scraped data was stored in a dictionary and saved to the local directory as a json. To run the program, the json was loaded into the main python script.  

*Summary:* 
Records available: 35 route names with 2-8 stations within each route
Records used: all
The primary attribute I used for this program were the station names as they served as the nodes to the graph. I did not incorporate the name of the individual routes into the program.

### Amtrak Station Information (CSV)
*Origin*  
This data came from Github user brentajones who cites their original source as the National Transportation Atlas Database, 2015. https://gist.github.com/brentajones/ced054626e8922cddd7009fdcea6b0a7
*Data Access*  
The Amtrak station information was accessed by downloading a csv file from brentajones’s Github repository. The headers were used as keys and the data were sorted into a dictionary.
*Summary:*  
Records available: 962 rows and 12 columns (X, Y, OBJECTID, STNCODE, STNNAME, ADDRESS1, ADDRESS2, CITY, STATE, ZIP, TYPE, STFIPS)
Records used: 529 rows (only TYPE = RAIL)
This dataset served as a foundational connection to connect the graph to the API. 
The X,Y fields represent the longitude and latitude of a station and were used to find hotels within the desired distance from the station. 
The STNNAME field corresponds to the name of different stations and is typically presented as a string of city and state. These values were used in the drop-down selection for the origin and destination of a trip. 
The CITY field is a string of the city where a train station is located. This field was used to gain information about the stations within the path as the cities match the names of the nodes in the graph.

## Google Nearby Search (API)
*Origin*  
Google servers
*Data Access*  
These data were accessed using an API key. The data were returned from the API as a JSON which I stored 
*Summary:*  
The inputs used were the geographic coordinates of the destination station, the user input maximum price, and the user input radius. “Lodging” was used as the default place type.
For each search, I utilized a maximum of 5 output results in my program. This was to limit the amount of options presented to the user and not make the information overwhelming.
For each result there are many fields available, such as photos, total user ratings, and opening hours (Figure 3). However, I kept the name, price level, rating, and vicinity fields to format an information output for the user. These were stored as attributes of a Hotel class object.

