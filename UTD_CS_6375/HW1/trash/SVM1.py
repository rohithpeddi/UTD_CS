#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 21:48:57 2020

@author: rohith
"""

import numpy as np
import pandas as pd
from cvxopt import matrix, spmatrix
from cvxopt.solvers import qp
from cvxopt import solvers

class LinearSVM():
	def __init__(self, C):
		self.C = C

	def fit(self, data, labels):
		Ft = data**2

		self.alpha = np.array(sol['x']).reshape(N,1)

		self.support_ = [i for i in xrange(N) if self.alpha[i] > 1e-3]
		self.w = (data * (self.alpha * labels)).sum(axis=0)
		for i in xrange(N):
			if 0 < self.alpha[i] < self.C:
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

svmclass = LinearSVM(1e-6)
svmclass.fit(X,Y)
print(svmclass.score(X,Y))




N = len(data)    
        Ft = data**2
        Ft = np.concatenate((data,Ft), axis=1)
        Ft1 = data**3
        Ft = np.concatenate((Ft, Ft1), axis=1)
        #Ft2 = X**4
        #Ft = np.concatenate((Ft, Ft2), axis=1)
        
        P = matrix(.5*(np.dot(labels,labels.T) * np.dot(Ft,Ft.T)))
        q = matrix(np.ones(N)* -1.)
        
        G = matrix(np.diag(np.ones(N)* -1.)) 
        h = matrix(np.zeros(N))
        
        A = matrix(Y.reshape(1, N)*1.)
        b = matrix(np.zeros(1))
        
        sol = solvers.qp(P,q,G,h,A,b)