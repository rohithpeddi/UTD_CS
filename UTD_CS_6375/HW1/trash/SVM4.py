#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 21:47:34 2020

@author: rohith
"""

import numpy as numpy
import pandas as pd
import cvxopt 

svm = pd.read_csv("mystery.data", names=["X1","X2","X3","X4","Y"])
X = svm.loc[:, "X1":"X4"]
#X['Xb'] = 1
X = X.values
Y = svm.loc[:, "Y":].values

case_n = len(X)   #1000
dim_n = len(X[0]) #784

# Prepare the matrices for the quadratic program
def getPrim(Z,y):
    case_n = len(Z)   #1000
    dim_n = len(Z[0]) #784
    P1 = numpy.asarray(numpy.diag(numpy.ones(dim_n)))
    P2 = numpy.zeros([1, dim_n]) #collect P2
    P3 = numpy.zeros([1, 1])
    Pup = numpy.concatenate((P1,P2.T),axis = 1)
    Pdown = numpy.concatenate((P2,P3),axis = 1)
    P = cvxopt.matrix(numpy.concatenate((Pup,Pdown), axis = 0))
    q = cvxopt.matrix(numpy.zeros([dim_n +1 ,1]))
    G = cvxopt.matrix(numpy.concatenate((Z*-1.,numpy.ones([case_n,1])*-1.), axis = 1))     #combine G1 G2
    h = cvxopt.matrix(numpy.zeros(case_n), tc='d')
    A = cvxopt.matrix(numpy.zeros([1, dim_n +1]))
    b = cvxopt.matrix(0.0)
    return P,q,G,h,A,b
        
P,q,G,h,A,b = getPrim(X, Y)
                
# Train the model (i.e. compute the alphas)
alpha = numpy.array(cvxopt.solvers.qp(P,q,G,h)['x']).flatten()

w_prim = alpha[:dim_n]
b_prim = alpha[dim_n:dim_n+1]

print alpha.shape
print w_prim.shape, b_prim