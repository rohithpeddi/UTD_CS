#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 20:41:38 2020

@author: rohith
"""
import numpy as np
import pandas as pd
import cvxopt

svm = pd.read_csv("mystery.data", names=["X1","X2","X3","X4","Y"])
X = svm.loc[:, "X1":"X4"].values
Y = svm.loc[:, "Y":].values

def fit(X, y, C):
    n_samples, n_features = X.shape
    # Compute the Gram matrix
    
    # construct P, q, A, b, G, h matrices for CVXOPT
    P = cvxopt.matrix(np.outer(y,y) * (np.dot(X,X.T)))
    q = cvxopt.matrix(np.ones(n_samples) * -1)
    A = cvxopt.matrix(y*-1., (1,n_samples))
    b = cvxopt.matrix(0.0)
    
    if C is None:      # hard-margin SVM
       G = cvxopt.matrix(np.diag(np.ones(n_samples) * -1))
       h = cvxopt.matrix(np.zeros(n_samples))
    else:              # soft-margin SVM
       G = cvxopt.matrix(np.vstack((np.diag(np.ones(n_samples) * -1), np.identity(n_samples))))
       h = cvxopt.matrix(np.hstack((np.zeros(n_samples), np.ones(n_samples) * C)))
    # solve QP problem
    solution = cvxopt.solvers.qp(P, q, G, h, A, b)
    # Lagrange multipliers
    a = np.ravel(solution['x'])
    display(solution)
    # Support vectors have non zero lagrange multipliers
    sv = a > 1e-5 # some small threshold
    
    
fit(X,Y, None)