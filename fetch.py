import requests
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import overpy
import geocoder
g = geocoder.ip('me')
print(g.latlng)


class Fetcher:
  def __init__(self, url):
    self.overpass_url = url
    
  def prepareQuery(data):
    area = data["area"]
    bbox = data["bbox"]
    node = data["node"]




if __name__ == "__main__":

  overpass_url = "http://overpass-api.de/api/interpreter"
  overpass_query = """
  [out:json];
  node(""" + str(52.2516399308433461 - 0.01) + "," + str(20.984026003823164 - 0.01) + ',' + str(52.251639930843346+ 0.01) + "," + str(20.984026003823164+ 0.01) + """);

  out center;
  """
  response = requests.get(overpass_url, 
                          params={'data': overpass_query})
  data = response.json()

  df = pd.json_normalize(data["elements"])
  df.to_excel("output1.xlsx")
  print(df["tags.amenity"].count())

  # Collect coords into list
  coords = []
  for element in data['elements']:
    if element['type'] == 'node':
      lon = element['lon']
      lat = element['lat']
      coords.append((lon, lat))
    elif 'center' in element:
      lon = element['center']['lon']
      lat = element['center']['lat']
      coords.append((lon, lat))
  # Convert coordinates into numpy array

  X = np.array(coords)
  plt.plot(X[:, 0], X[:, 1], 'o')
  plt.title('')
  plt.xlabel('Longitude')
  plt.ylabel('Latitude')
  plt.axis('equal')
  plt.show()