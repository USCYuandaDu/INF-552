import sys 
import numpy as np
from sklearn import linear_model

regr = linear_model.LinearRegression()
filename = sys.argv[1]
data = np.loadtxt(filename, dtype = "float", delimiter = ",")
X = np.mat(data[:,0:2])
m,n = np.shape(X)
ones = np.ones((m,1))
X = np.concatenate((ones, X), axis = 1)
Y = data[:,2]
Y = np.mat(Y[:, np.newaxis])
regr.fit(X, Y)
res = regr.coef_
res[0][0] = regr.intercept_
print res
