from collections import defaultdict
import numpy as np
from numpy import genfromtxt
import random

amplitude =[] 
means =[]
covariance =[]
       
def E_step(data, K):
    N = len(data)
    pdfs = np.empty([N,K])

    for i in xrange(0,K):
        m=means[i]
        cov=covariance[i]
        invcov=np.mat(np.linalg.inv(cov))
        norm_factor = 1 / np.sqrt((2*np.pi)**2 * np.linalg.det(cov))
        for row in xrange(0,N):
            tmp = np.mat(data[row,:] - m)
            val = norm_factor*np.exp(-0.5*tmp*invcov*tmp.T)
            pdfs[row][i] = val[0][0]

    weights = np.empty([N,K])
    for i in xrange(0,N):
        denominator=np.sum(amplitude*pdfs[i])
        for j in xrange(0,K):
            weights[i][j]=amplitude[j]*pdfs[i][j] / denominator
    return weights

def M_step(data,membership_weights,K):
    global means,covariance,amplitude

    means =[]
    covariance =[]
    amplitude = []
    N = len(data)
    dimension = len(data[0])

    if membership_weights is None:
        amplitude = np.ones(K) / K
        amplitude = amplitude.tolist()
        clusters = kmeans(data)
        for i in xrange(0,K):
            means.append(np.mean(clusters[i], axis=0))
            covariance.append(np.cov(clusters[i].T))
    else:
        amplitude = np.sum(membership_weights, axis=0) / N
        for i in xrange(0,K):
            means.append(np.sum(np.multiply(data,membership_weights[:,i].reshape(len(data),1)),axis=0) / sum(membership_weights[:,i]))
            cov_temp_sum=np.zeros((dimension,dimension))
            for j in xrange(0,N):
                temp=data[j]-means[i]
                temp=np.dot(temp.T.reshape(dimension,1),temp.reshape(1,dimension))
                temp=temp*membership_weights[j][i]
                cov_temp_sum=np.add(cov_temp_sum,temp)
            cov_temp_sum=cov_temp_sum / np.sum(membership_weights[:,i])
            covariance.append(cov_temp_sum)
    return 

def kmeans(data):
    centroids = np.array(random.sample(data, 3))
    dict_of_clusters=defaultdict(list)
    for i in xrange(0,len(data)):
        val, min_index = min((val, idx) for (idx, val) in enumerate([compute_distance(data[i],x) for x in centroids]))
        dict_of_clusters[min_index].append(data[i].tolist())
    dict_of_clusters=[np.array(dict_of_clusters[i]) for i in dict_of_clusters]
    return dict_of_clusters
    
def compute_distance(x,y):
    return np.sqrt(np.sum((x-y)**2))

if __name__ == "__main__":        
    data = genfromtxt('clusters.txt', delimiter=',')
    threshold = 0.0001
    max_iteration = 500
    K = 3
    count = 1

    current_weights=None
    while True:
        M_step(data,current_weights, K)
        new_weights = E_step(data, K)
        
        #print 'new_membership_weights', new_weights

        # if exceed max iterations then stop
        if count >= max_iteration:
            break

        # if weight have changed below threshold , also stop
        if current_weights is not None and new_weights is not None and (np.abs(new_weights-current_weights) < threshold).all():
            break

        count+= 1
        current_weights=new_weights
    
    print "Amplitudes:"
    print amplitude
    print "\nMeans:"
    print np.array(means)
    print "\nCovariances:"
    print np.array(covariance)


