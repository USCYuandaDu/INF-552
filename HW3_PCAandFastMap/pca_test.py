import sys
import numpy as np
from sklearn.decomposition import PCA


filename = sys.argv[1]
k = int(sys.argv[2])
from sklearn.decomposition import PCA
X = np.array([[-1, 1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
pca=PCA(n_components=1)
pca.fit(X)
print pca.transform(X)
