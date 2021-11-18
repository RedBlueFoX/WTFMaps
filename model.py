import pandas as pd
import json
import geocoder
import math
from haversine import haversine, Unit
from fetch import Fetcher
from preprocessing import PData

amenitiesList = ("bar", "biergarten", "cafe", "fast_food", "food_court", "ice_cream", "pub", "restaurant",
	"bus_station", "taxi", "arts_centre", "events_venue", "fountain", "planetarium", "theatre", "townhall",
	 "clock","dive_centre", "monastery", "place_of_worship")
foodCategoryList = ("bar", "biergarten", "cafe", "fast_food", "food_court", "ice_cream", "pub", "restaurant")
activityCategoryList = ("arts_centre", "events_venue","fountain", "planetarium","theatre","townhall","clock",
	"dive_centre","monastery","place_of_worship", "aquarium", "artwork", "attraction", "gallery", "museum",
	 "theme_park", "viewpoint", "zoo")
def model(response, userData, coordinates):
	eligibleData = filterEligibleData(response)
	distances = []
	for index, row in eligibleData.iterrows():
		distances.append(calculateDistance((row["lat"], row["lon"]),coordinates))
	eligibleData["distance"] = distances
	categoriziedData = categorization(eligibleData)
	print(categoriziedData.to_string())
def calculateDistance(coordinatesA, coordinatesB):
	return haversine(coordinatesA, coordinatesB, unit = Unit.KILOMETERS)

def filterEligibleData(response):
	df = pd.json_normalize(response["elements"])
	maskT = pd.notnull(df['tags.tourism'])
	maskA = pd.notnull(df['tags.amenity'])
	mask = [any(tup) for tup in zip(maskT, maskA)]
	result = df[mask]
	result = result[["lat", "lon", "tags.name:en", "tags.addr:city", "tags.amenity", "tags.tourism"]]
	for index, row in result.iterrows():
		if row["tags.amenity"] not in amenitiesList:
			if(pd.isna(row["tags.tourism"])):
				result.drop(index, axis = 0,inplace = True)

	result["tags.amenity"] = result["tags.amenity"].combine_first(result["tags.tourism"])
	result = result[["lat", "lon", "tags.amenity"]]
	return result

def categorization(data):
	categories = []
	for index, row in data.iterrows():
		if(row["tags.amenity"] in foodCategoryList):
			categories.append("Food")
		elif(row["tags.amenity"] in activityCategoryList):
			categories.append("Activity")
		else:
			categories.append("Undefined")
	data["Category"] = categories
	return data	


def main():
	fetcher = Fetcher()
	g = geocoder.ip('me')
	print(g.latlng)
	coordinates = (g.latlng[0],g.latlng[1])
	fetcher.prepareQuery(coordinates, 5)
	response_data = fetcher.request()

	f = open("static/sampleExample.json",)
	jsonData = json.load(f, strict = False)
	preprocessor = PData(jsonData)

	user_data = preprocessor.getData()
	model(response_data, preprocessor, coordinates)

if __name__ == '__main__':
	main()
