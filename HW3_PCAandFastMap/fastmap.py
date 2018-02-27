import sys 
import numpy as np

#parse the input file and create the graph for it
#return the original data and int[][] graph
def parseAndCreateGraph(filename):
	data = np.loadtxt(filename, dtype = "int", delimiter = "\t")
	graph = {}
	for line in data:
		node1 = line[0]
		node2 = line[1]
		distance = line[2]
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
	return node1, node2, maxDis




filename = sys.argv[1]
data, graph = parseAndCreateGraph(filename)
pickTheMaxDistance(data, graph)
