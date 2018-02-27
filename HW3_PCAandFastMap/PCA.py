import sys
import numpy as np


filename = sys.argv[1]
k = int(sys.argv[2])
data = np.loadtxt(filename, dtype = "float", delimiter = "\t")
data = np.mat(data)
mean = np.mean(data, axis = 0)
data = data - mean
cov = np.cov(data, rowvar = False)
eigenVal, eigenVac = np.linalg.eig(cov)
eigenValInd = np.argsort(eigenVal)[:-(k+1):-1]
redEigenVac = np.mat(eigenVac[:, eigenValInd])
reduced_data = data * redEigenVac
print reduced_data