import sys
import numpy as np


filename = sys.argv[1]
k = int(sys.argv[2])
rawData = np.loadtxt(filename, dtype = "float", delimiter = "\t")
rawData = np.mat(rawData)
mean = np.mean(rawData, axis = 0)
data = rawData - mean
cov = np.cov(data, rowvar = False)
eigenVal, eigenVac = np.linalg.eig(cov)
eigenValInd = np.argsort(eigenVal)[:-(k+1):-1]
redEigenVac = np.mat(eigenVac[:, eigenValInd])
print redEigenVac
