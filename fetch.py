import requests
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import overpy




class Fetcher:
  def __init__(self):
    self.overpass_url = "http://overpass-api.de/api/interpreter"
    
  def prepareQuery(self, coordinates, scale):
    self.overpass_query = """
  [out:json];
  node(""" + str(coordinates[0] - (scale / 100)) + "," + str(coordinates[1] - (scale / 100)) + ',' + str(coordinates[0]+ (scale / 100)) + "," + str(coordinates[1] + (scale / 100)) + """);

  out center;
  """
  def request(self):
    response = requests.get(self.overpass_url, params = {'data': self.overpass_query})
    self.data = response.json()
    return self.data




if __name__ == "__main__":



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