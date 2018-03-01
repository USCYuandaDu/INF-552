import random
import numpy as np
import sys
from numpy import genfromtxt
from collections import defaultdict

K_centroids = None
max_iteration = 100
threshold = 0.001
        
def update_centroids(data, centroids):
    dict_of_clusters = defaultdict(list)
    
    for i in xrange(0,len(data)):
        val, min_index = min((val, idx) for (idx, val) in enumerate([compute_distance(data[i],x) for x in centroids]))

        dict_of_clusters[min_index].append(data[i].tolist())

    new_centroids=[]
    for cluster in dict_of_clusters:
    	#print cluster
        new_centroids.append( np.array(dict_of_clusters[cluster]).mean(axis=0))

    return new_centroids

def compute_distance(x,y):   
    return np.sqrt(np.sum((x-y)**2))

if __name__ == "__main__":
    data = genfromtxt('clusters.txt', delimiter=',')

    count = 1
    #randomly select 3 nodes as original centroids
    K_centroids = np.array(random.sample(data, 3))
        
    while True:
        new_centroids = np.array(update_centroids(data,K_centroids))

        # if maximation number exceeds, or new centroids completely equals old ones, or blow threshold
        if count >= max_iteration or np.array_equal(K_centroids,new_centroids) or (np.abs(new_centroids - K_centroids) < threshold).all():
            #print "number of interations:",count
            print "Cluster Centroids:"
            print new_centroids
            break 

        count+= 1
        K_centroids = new_centroids





