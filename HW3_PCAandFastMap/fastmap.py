import sys 
import numpy as np

#assumption: ID is not sequential so that use a map to build the graph instead of array
#assumptino: the printed data is finally result, a map, the key is ID and the value is the value of the coordinate system

#parse the input file and create the graph for it
#return the original data and int[][] graph
def parseAndCreateGraph(filename):
	data = np.loadtxt(filename, dtype = "int", delimiter = "\t")
	graph = {}
	for line in data:
		node1 = line[0]
		node2 = line[1]
		distance = float(line[2])
		if(node1 not in graph):
			graph[node1] = {}
		if(node2 not in graph):
			graph[node2] = {}
		graph[node1][node2] = distance
		graph[node2][node1] = distance
	return data, graph

#choose the maxDis of node1 and node2
#heuristic method
def pickTheMaxDistance(data, graph):
	maxDis = 0
	node1 = 0
	node2 = 0
	curNode = data[0][0]
	for i in range(5):
		for neighbor in graph[curNode]:
			curDis = graph[curNode][neighbor]
			if(curDis > maxDis):
				maxDis = curDis
				node1 = min(curNode, neighbor)
				node2 = max(curNode, neighbor)
			elif(curDis == maxDis):
				if(min(curNode, neighbor) < node1):
					node1 = min(curNode, neighbor)
					node2 = max(curNode, neighbor)
		curNode = node1 if curNode == node2 else node2
	if(maxDis == 0):
		raise Exception("k is not valid, because maxDis is equal to 0 at this step")
	return node1, node2, maxDis
#fastMap one step
def fastMap(node1, node2, maxDis, graph, data, redData):
	for node in graph:
		dis_ia = 0
		dis_ib = 0
		if(node != node1):
			dis_ia = graph[node][node1]
		if(node != node2):
			dis_ib = graph[node][node2]
		cur_val = (dis_ia ** 2 + maxDis ** 2 - dis_ib ** 2) / (2 * maxDis)
		if node not in redData:
			redData[node] = []
		redData[node].append(cur_val)
	return redData
#update the distance
def updateDis(graph, data, redData):
	for line in data:
		node1 = line[0]
		node2 = line[1]
		originDis = graph[node1][node2]
		newDis = originDis ** 2 - (redData[node1][-1] - redData[node2][-1]) ** 2
		if(newDis < 0):
			raise Exception("the k is not valid, too big")
		newDis = newDis ** 0.5
		graph[node1][node2] = newDis
		graph[node2][node1] = newDis
try:
	filename = sys.argv[1]
	k = int(sys.argv[2])
	data, graph = parseAndCreateGraph(filename)
	redData = {}
	for i in range(k):
		node1, node2, maxDis = pickTheMaxDistance(data, graph)
		fastMap(node1, node2, maxDis, graph, data, redData)
		updateDis(graph, data, redData)
	print redData
except Exception as error:
	print error










