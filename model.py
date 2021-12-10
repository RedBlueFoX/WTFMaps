import pandas as pd
import json
import geocoder
import math
from haversine import haversine, Unit
from fetch import Fetcher
from preprocessing import PData
import openrouteservice
from geojson import dump
pd.options.mode.chained_assignment = None


amenitiesList = ("bar", "biergarten", "cafe", "fast_food", "food_court", "ice_cream", "pub", "restaurant",
	"bus_station", "taxi", "arts_centre", "events_venue", "fountain", "planetarium", "theatre", "townhall",
	 "clock","dive_centre", "monastery", "place_of_worship")
foodCategoryList = ("bar", "biergarten", "cafe", "fast_food", "food_court", "ice_cream", "pub", "restaurant")
activityCategoryList = ("arts_centre", "events_venue","fountain", "planetarium","theatre","townhall","clock",
	"dive_centre","monastery","place_of_worship", "aquarium", "artwork", "attraction", "gallery", "museum",
	 "theme_park", "viewpoint", "zoo")
def model(response, userData, coordinates, time):
	listOfResults = []
	eligibleData = filterEligibleData(response)
	distances = []
	maxDistance = 0
	for index, row in eligibleData.iterrows():
		temp = calculateDistance((row["lat"], row["lon"]),coordinates)
		distances.append(temp)
		if(temp > maxDistance):
			maxDistance = temp
	eligibleData["distance"] = distances
	categoriziedData = categorization(eligibleData)
	# print(categoriziedData[["lat", "lon", "tags.amenity"]].to_string())
	weights = []
	for index, row in categoriziedData.iterrows():
		weights.append(giveWeights(row, userData, maxDistance))
	categoriziedData["Weights"] = weights
	# print(categoriziedData[["lat", "lon", "tags.amenity", "Weights"]].to_string())
	priorityList = pd.DataFrame()
	while time > 0:
		priorityList = prioritize(categoriziedData, priorityList)
		time = time - 0.5
	print(priorityList[["lat", "lon", "tags.amenity", "Weights", "distance","tags.name"]].to_string())
	outputCoordList = []
	for index, row in priorityList.iterrows():
		outputCoordList.append((row["lon"], row["lat"]))
	return priorityList, outputCoordList

	
	
	
def prioritize(inputData, outList):
	inputData["Weights"].fillna(0)
	tempIndex = [inputData["Weights"].idxmax()]

	outList = outList.append(inputData.loc[tempIndex])
	inputData.drop(tempIndex, inplace = True)
	return outList
			

def calculateDistance(coordinatesA, coordinatesB):
	return haversine(coordinatesA, coordinatesB, unit = Unit.KILOMETERS)
def sigmoid(x):
	# return 1/(1 + math.exp(-x))
	return math.cos(x) 
def giveWeights(row, userWeights, maxDistance):
	if row["Category"] in foodCategoryList:
		sFoodWeights = 0.5
		nCuisineWeights = 0.5
		restaurantsWeights = 0.5
		fFoodWeights = 0.5
		if row["Category"] in ("bar", "biergarten", "pub"):
			sFoodWeights = sFoodWeights * userWeights.index[userWeights["FoodsStreetfood"]] * sigmoid(row["Distance"] / maxDistance)
			return sFoodWeights
		if row["Category"] in ("cafe", "food_court", "fast_food"):
			fFoodWeights = fFoodWeights * userWeights.index[userWeights["FoodsFastFood"]] * sigmoid(row["Distance"] / maxDistance)
			return fFoodWeights
		if row["Category"] in ("restaurant"):
			restaurantsWeights = (nCuisineWeights * userWeights.index[userWeights["FoodsNationalCuisine"]] * sigmoid(row["distance"] / maxDistance)
				+ restaurantsWeights * userWeights.index[userWeights["FoodsRestaurant"]] * sigmoid(row["distance"] / maxDistance)) / 2
			return restaurantsWeights

	return (0.5 + sigmoid(row["distance"] / maxDistance)) / 2




def filterEligibleData(response):
	df = pd.json_normalize(response["elements"])
	maskT = pd.notnull(df['tags.tourism'])
	maskA = pd.notnull(df['tags.amenity'])
	mask = [any(tup) for tup in zip(maskT, maskA)]
	result = df[mask]

	for index, row in result.iterrows():
		if row["tags.amenity"] not in amenitiesList:
			if(pd.isna(row["tags.tourism"])):
				result.drop(index, axis = 0,inplace = True)

	result["tags.amenity"] = result["tags.amenity"].combine_first(result["tags.tourism"])
	# result = result[["lat", "lon", "tags.amenity"]]
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
	priorityDF, coordList = model(response_data, preprocessor, coordinates, 3)
	tokenf = open("osmtoken.txt",)
	token = tokenf.readline()

	client = openrouteservice.Client(key = token)
	routes = client.directions(coordList, profile = 'cycling-regular', optimize_waypoints = True)

	print(routes)
	with open("output.geojson", "w") as f:
		dump(routes, f)

if __name__ == '__main__':
	main()
