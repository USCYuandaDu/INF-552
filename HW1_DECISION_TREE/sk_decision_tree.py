import re
import numpy as np
from sklearn import tree

mapX = {0:{"Low":0, "Moderate":1, "High":2}, 1:{"Cheap":0,"Normal":1,"Expensive":2}, 2:{"Loud":1,"Quiet":0}, 3:{"Talpiot":0,"City-Center":1, "German-Colony":2, "Ein-Karem":3, "Mahane-Yehuda":4}, 4:{"Yes":1, "No":0}, 5:{"Yes":1, "No":0}}
mapY = {"Yes":1, "No":0}

def convertXLine(line):
	res = []
	for i in range(len(line)):
		res.append(mapX[i][line[i]])
	return res

def convertYLine(line):
	res = []
	for i in range(len(line)):
		res.append(mapY[line[i]])
	return res

with open("dt-data.txt", "r") as myfile:
	raw = myfile.read()
data = re.findall(r"[0-9]+: (.*);", raw)
data = [line.split(", ") for line in data]
data = np.array(data)
dataX = data[:, :-1]
dataY = data[:, -1]

dataXX = [convertXLine(line) for line in dataX]
dataYY = convertYLine(dataY)
predictXX = [[1,0,1,1,0,0]]

clf = tree.DecisionTreeClassifier()
clf = clf.fit(dataXX, dataYY)
print clf.predict(predictXX)
