import numpy as np
import pandas as pd
from cvxopt import matrix as matrix
from cvxopt import solvers as solvers

class LinearSVM():    
    def __init__(self, C):
		self.C = C
        
    def kernel(self,x):
        x = x.reshape(1,4)
        return np.concatenate((np.dot(x.T, x).reshape(1,16), x), axis=1).reshape(1,20).tolist()
        
    def fit(self, data, labels):
        N = len(data)    
        
        Ft = data**2
        Ft = np.concatenate((data,Ft), axis=1)
        Ft1 = data**3
        Ft = np.concatenate((Ft, Ft1), axis=1)
        #Ft6 = X*np.flip(X, axis=1)
        #Ft = np.concatenate((Ft, Ft6), axis=1)
        Ft2 = X**4
        Ft = np.concatenate((Ft, Ft2), axis=1)
        Ft3 = X**5
        Ft = np.concatenate((Ft, Ft3), axis=1)
        Ft4 = X**6
        Ft = np.concatenate((Ft, Ft4), axis=1)
        Ft5 = X**7
        Ft = np.concatenate((Ft, Ft5), axis=1)
        
        P = matrix(.5*(np.dot(labels,labels.T) * np.dot(Ft,Ft.T)))
        q = matrix(np.ones(N)* -1.)
        
        G = matrix(np.diag(np.ones(N)* -1.)) 
        h = matrix(np.zeros(N))
        
        A = matrix(Y.reshape(1, N)*1.)
        b = matrix(np.zeros(1))
        
        sol = solvers.qp(P,q,G,h,A,b)
        
        self.alpha = np.array(sol['x']).reshape(N,1)
        self.support_ = [i for i in xrange(N) if self.alpha[i] > 1e-3]
        self.w = (data * (self.alpha * labels)).sum(axis=0)
        
        for i in xrange(N):
			if 1e-1 < self.alpha[i] < self.C:
				self.bias = labels[i] - np.dot(self.w, data[i])
				break            
    
    def predict(self, data):
		if len(data.shape) <= 1:
			self.predict(data.reshape(1, data.shape[0]))

		return np.sign(np.dot(data, self.w) + self.bias)
    
    def decision_function(self, data):
		return (np.dot(data, self.w) + self.bias) / np.linalg.norm(self.w)

    def score(self, data, labels):
		pr = self.predict(data)
		correct = 0.
		N = len(data)
		for i in xrange(N):
			correct += 1 if pr[i] * labels[i] > 0 else 0
		return correct / N

svm = pd.read_csv("mystery.data", names=["X1","X2","X3","X4","Y"])
X = svm.loc[:, "X1":"X4"].values
Y = svm.loc[:, "Y":].values

svmclass = LinearSVM(100000)
svmclass.fit(X,Y)
print('SCORE: ', svmclass.score(X,Y))
print('SUPPORT VECTORS: ', len(svmclass.support_))
print('BIAS: ', svmclass.bias)
print('ALPHAS : ', svmclass.alpha[(svmclass.alpha>1e-6).ravel()])
print('WEIGHTS: ', svmclass.w)
print('MARGIN: ', np.dot(svmclass.w, svmclass.w.T))