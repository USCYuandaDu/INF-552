import sys 
import numpy as np


filename = sys.argv[1]
data = np.loadtxt(filename, dtype = "float", delimiter = ",")
X = np.mat(data[:,0:2])
Y = data[:,2]
Y = np.mat(Y[:, np.newaxis])
xTx = X.T * X
if (np.linalg.det(xTx) == 0):
	print "This matrix is singular, cannot do inverse"
w = xTx.I * (X.T * Y)
w = w.T
print w

