import sys 
import numpy as np


filename = sys.argv[1]
data = np.loadtxt(filename, dtype = "float", delimiter = ",")
print data
