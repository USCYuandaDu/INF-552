import sys
import numpy as np
from sklearn.decomposition import PCA


filename = sys.argv[1]
k = int(sys.argv[2])
data = np.loadtxt(filename, dtype = "float", delimiter = "\t")
data = np.mat(data)
mean = np.mean(data, axis = 0)
data = data - mean
pca=PCA(n_components=k, svd_solver='arpack')
pca.fit(data)
print pca.components_.T
