import numpy as np
import cvxopt
import matplotlib.pyplot as plt
from numpy import linalg

class NonLinearSVM:

	def poly_transform(self, x, y):
		return [1, x**2, y**2, np.sqrt(2)*x,  np.sqrt(2)*y, np.sqrt(2)*x*y]
	
	def fit(self, X, Y):
		rows, cols = X.shape
		transformed_X=np.zeros((100,6))
		for i in range(0,len(X)):
			transformed_X[i]=self.poly_transform(X[i][0],X[i][1])

		rows, cols = transformed_X.shape
		Q = np.zeros((rows, rows))
		for i in range(rows):
			for j in range(rows):
				Q[i,j] = np.dot(transformed_X[i], transformed_X[j])
		P = cvxopt.matrix(np.outer(Y,Y) * Q)
		q = cvxopt.matrix(np.ones(rows) * -1)
		A = cvxopt.matrix(Y, (1,rows))
		b = cvxopt.matrix(0.0)

		G = cvxopt.matrix(np.diag(np.ones(rows) * -1))
		h = cvxopt.matrix(np.zeros(rows))

		alphas = np.array(cvxopt.solvers.qp(P, q, G, h, A, b)['x']).reshape(1,rows)[0]

		valid_alphas=alphas>0.00001
		support_vector_indices = np.where(valid_alphas)[0]

		self.alphas = alphas[support_vector_indices]
		self.support_vectors = transformed_X[support_vector_indices]
		self.support_vectors_y = Y[support_vector_indices]
		print("%d support vectors out of %d points" % (len(self.alphas), rows))
		
		self.weights = np.zeros(cols)
		for i in range(len(self.alphas)):
			self.weights += self.alphas[i] * self.support_vectors_y[i] * self.support_vectors[i]

		self.intercept = self.support_vectors_y[0] - np.dot(self.weights, self.support_vectors[0])
		
def main():
	data=np.loadtxt('nonlinsep.txt',dtype='float',delimiter=',')
	X=data[:,0:2]
	Y=data[:,2]
	p=NonLinearSVM()
	p.fit(X,Y)
	print("Intercept:")
	print(p.intercept)
	print("Weights:")
	print(p.weights)

if __name__ == "__main__":
		main()
	
	   
