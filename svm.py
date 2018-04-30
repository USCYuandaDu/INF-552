import numpy as np
import cvxopt
import matplotlib.pyplot as plt
import sys

class LinearSVM:

	def __init__(self, X, Y, isLinear):

		self.isLinear = isLinear
		self.X = X
		self.Y = Y
		self.rows, self.cols = X.shape
		self.omiga = 0.01

	def generateKernel(self):
		self.kernel = np.empty((self.rows, self.rows))
		if(self.isLinear):
			for i in range(self.rows):
				for j in range(self.rows):
					self.kernel[i, j] = np.dot(self.X[i], self.X[j])
		else:
			for i in range(self.rows):
				for j in range(self.rows):
					self.kernel[i, j] = (1 + self.omiga * np.dot(self.X[i], self.X[j])) ** 2
			# self.kernel = np.dot()
	def fit(self):

		self.generateKernel()

		Q = np.zeros((self.rows, self.rows))
		for i in range(self.rows):
			for j in range(self.rows):
				Q[i,j] = self.kernel[i, j]

		P = cvxopt.matrix(np.outer(self.Y,self.Y) * Q)
		q = cvxopt.matrix(np.ones(self.rows) * -1)
		A = cvxopt.matrix(self.Y, (1,self.rows))
		b = cvxopt.matrix(0.0)

		G = cvxopt.matrix(np.diag(np.ones(self.rows) * -1))
		h = cvxopt.matrix(np.zeros(self.rows))

		alphas = np.array(cvxopt.solvers.qp(P, q, G, h, A, b)['x']).reshape(1,self.rows)[0]

		self.support_vector_indices = np.where(alphas>0.00001)[0]


		self.alphas = alphas[self.support_vector_indices][:, np.newaxis]
		self.support_vectors = self.X[self.support_vector_indices]
		self.support_vectors_y = self.Y[self.support_vector_indices][:, np.newaxis]
		print("%d support vectors out of %d points" % (len(self.alphas), self.rows))

		sv_x0 = self.X[self.support_vector_indices[0]]
		sv_y0 = self.Y[self.support_vector_indices[0]]
		sv_n = len(self.support_vectors)
		self.zz0 = np.empty((sv_n, 1))
		for i in range(sv_n):
			self.zz0[i] = self.kernel[self.support_vector_indices[i], self.support_vector_indices[0]]
		self.intercept = sv_y0 - np.sum(self.alphas * self.support_vectors_y * self.zz0, 0)

		if(self.isLinear):
			self.weights = np.zeros((1, self.cols))
			self.weights = np.sum(self.alphas * self.support_vectors_y * self.support_vectors, 0)[:, np.newaxis]

			print("Weights:")
			print(self.weights)

		print("Intercept:")
		print(self.intercept)
	def predictX2(self, inputX):
		outputY = []
		for x in inputX:
			outputY.append(-(self.weights[0, 0] * x + self.intercept[0]) / self.weights[1, 0])
		return outputY

	def predictNonLinear(self, inputX):

		predict = []
		for x in inputX:
			sv_n = len(self.support_vectors)
			zzn = np.empty((sv_n, 1))
			for i in range(sv_n):
				z_sv = self.support_vectors[i]
				zzn[i] = (1 + self.omiga * np.dot(z_sv, x)) ** 2
			if(np.sum(self.alphas * self.support_vectors_y * zzn, 0) + self.intercept > 0):
				predict.append(1)
			else:
				predict.append(0)
		return np.array(predict)


	def displayLin(self):
		plt.scatter(self.X[:,0],self.X[:,1],c=self.Y,cmap='bwr',alpha=1,s=50,edgecolors='k')			
		plt.scatter(self.support_vectors[:,0],self.support_vectors[:,1],facecolors='none',s=100, edgecolors='k')
		inputX = np.linspace(0 , 1, 11)
		plt.plot(inputX, self.predictX2(inputX))
		plt.show()

	def displayNonLin(self):
		print "Support_vectors:"
		print self.support_vectors
		print self.support_vectors_y
		plt.scatter(self.X[:,0],self.X[:,1],c=self.Y,cmap='bwr',alpha=1,s=50,edgecolors='k')			
		plt.scatter(self.support_vectors[:,0],self.support_vectors[:,1],facecolors='none',s=100, edgecolors='k')
		h = 0.1
		x_min, x_max = -10,10
		y_min, y_max = -10,10
		xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
		    np.arange(y_min, y_max, h))
		inputX = np.array([xx.ravel(), yy.ravel()]).T
		Z = self.predictNonLinear(inputX)
		Z = Z.reshape(xx.shape)
		plt.contourf(xx, yy, Z, cmap=plt.cm.Paired, alpha=0.8)
		plt.show()	

	def display(self):
		if(self.isLinear):
			self.displayLin()
		else:
			self.displayNonLin()

def main():

	if(sys.argv[1] == "linear"):
		data = np.loadtxt('linsep.txt',dtype='float',delimiter=',')
		X = data[:,0:2]
		Y = data[:,2]
		p = LinearSVM(X, Y, True)
		p.fit()
		p.display()
	else:
		data = np.loadtxt('nonlinsep.txt',dtype='float',delimiter=',')
		X = data[:,0:2]
		Y = data[:,2]
		p = LinearSVM(X, Y, False)
		p.fit()
		p.display()		

if __name__ == "__main__":
	main()




