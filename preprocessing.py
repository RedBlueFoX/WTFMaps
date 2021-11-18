import json
import pandas as pd

class PData:
	data = []
	names = []
	pddata = []
	categories = []
	def __init__(self, jsonInput):
		for i in jsonInput['contents']:
			
			if(i["Type"] == "Choice"):
				for j in range(i["Total"]):
					self.categories.append(i["Category"])
					temp_string = (i["Name"] + i["Answers"][j])
					new_string = ''.join(char for char in temp_string if char.isalnum())
					self.names.append(new_string)
				for j in range(i["Total"]):
					if(i["Answer"] != j + 1):
						self.data.append(0.25)
					elif(i["Answer"] == j + 1):
						self.data.append(0.75)
			elif(i["Type"] == "Scale"):
				self.names.append(i["Name"])
				self.categories.append(i["Category"])
				self.data.append(0.2 * i["Answer"])

		self.pddata = pd.DataFrame()
		self.pddata["Name"] = self.names
		self.pddata["Caregory"] = self.categories
		self.pddata["Weights"] = self.data
		
	def print(self):
		print(self.pddata)
	def getData(self):
		return self.pddata

if __name__ == '__main__':
	file = open("static/sampleExample.json")
	jsonData = json.load(file, strict = False)
	data = PData(jsonData)
	data.print()