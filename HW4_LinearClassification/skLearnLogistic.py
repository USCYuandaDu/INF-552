import sys 
import numpy as np
from sklearn.linear_model import LogisticRegression


filename = sys.argv[1]
data = np.loadtxt(filename, dtype = "float", delimiter = ",")
X = data[:,0:3]
Y = data[:,4]
Y = Y[:, np.newaxis]
m, n = np.shape(X)
ones = np.ones((m,1))
X = np.concatenate((ones, X), axis = 1)
classifier = LogisticRegression()
classifier.fit(X, Y)

weights = classifier.coef_
predict = np.dot(X, weights.T)
res = np.ones((m,1));
res[predict < 0] = -1
res = np.multiply(res, Y)
res[res < 0] = 0
print np.sum(res, axis=0)[0] / float(m)
print classifier.coef_