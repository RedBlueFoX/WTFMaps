import requests
import json
import numpy as np
import matplotlib.pyplot as plt
import overpy
from overpassify import overpassify

overapi = overpy.Overpass()

@overpassify
def query(bbox):
  search = Bbox(Bbox.S, Bbox.W, Bbox.N, Bbox.E)
  nodes = Node(search)
  out(nodes, geom = False, count = True)
  noop()

bbox = {
   S: 50.745,
   W: 7.17,
   N: 50.75,
   E: 7.18
}
overapi.query(query(bbox))
# class Fetcher:
#   def __init__(self, url):
#     self.overpass_url = url
    
#   def request_query(self, query):

#     return requests.get(self.overpass_url, params={'data': query}).json()
#   def request_bbox(bbox):

#   def request_location(point, radius):


# if __name__ == "__main__":

#   overpass_url = "http://overpass-api.de/api/interpreter"
#   overpass_query = """
#   [out:json];
#   area["ISO3166-1"="KP"][admin_level=2];
#   (node["place"="city"](area);
#    way["place"="city"](area);
#    rel["place"="city"](area);
#   );
#   out center;
#   """
#   response = requests.get(overpass_url, 
#                           params={'data': overpass_query})
#   data = response.json()


#   # Collect coords into list
#   coords = []
#   for element in data['elements']:
#     if element['type'] == 'node':
#       lon = element['lon']
#       lat = element['lat']
#       coords.append((lon, lat))
#     elif 'center' in element:
#       lon = element['center']['lon']
#       lat = element['center']['lat']
#       coords.append((lon, lat))
#   # Convert coordinates into numpy array
#   X = np.array(coords)
#   plt.plot(X[:, 0], X[:, 1], 'o')
#   plt.title('')
#   plt.xlabel('Longitude')
#   plt.ylabel('Latitude')
#   plt.axis('equal')
#   plt.show()