# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 20:29:06 2020

@author: ROHITH PEDDI
"""

import numpy as np
import pandas as pd
import cvxopt as cvxopt

data_train = pd.read_csv('sonar_train.data', header = None).values
data_val = pd.read_csv('sonar_valid.data', header = None).values
data_test = pd.read_csv('sonar_test.data', header = None).values

M, N = data_train.shape

data_train[data_train[:, N-1] == 2, N-1] = -1
data_val[data_val[:, N-1] == 2, N-1] = -1
data_test[data_test[:, N-1] == 2, N-1] = -1

###############################################################################
############################ SVM IMPLEMENTATION ###############################
###############################################################################

class SVM(object):
    
    def __init__(self):
        return
        
    def train(self, X, Y, c):        
        NUM, DIM = X.shape    
        P = cvxopt.matrix(np.concatenate((np.eye(NUM+DIM+1, M=DIM).T, np.zeros((NUM+1,NUM+DIM+1))), axis = 0))
        q = cvxopt.matrix(np.concatenate((np.concatenate((np.zeros((DIM,1)), np.zeros((1,1))), axis=0), c*np.ones((NUM,1))), axis = 0))
        
        G_si = np.concatenate((-1*np.eye(NUM), -1*np.eye(NUM)), axis = 0)
        G_b = np.concatenate((-1.* Y, np.zeros((NUM,1))), axis = 0)
        G_x = np.concatenate((-1.*X*Y, np.zeros((NUM, DIM))), axis = 0)
               
        G_com = np.concatenate((G_x, G_b), axis=1)
        
        G = cvxopt.matrix(np.concatenate((G_com, G_si), axis=1))    
        h = cvxopt.matrix(np.concatenate((-1.*np.ones((NUM, 1)), np.zeros((NUM,1))), axis=0))        
           
        return cvxopt.solvers.qp(P, q, G, h)
    
    def score(self, W, X, Y, bias):    
        pred = (np.dot(X, W) + bias) * Y 
        pred[pred>=0] = 0
        pred[pred<0] = 1
        return np.sum(pred)
    
    def fit_svm(self, X_train, Y_train, X_val, Y_val, X_test, Y_test, k, c):        
        print('CALCULATING SVM SOLUTION FOR c ', c, ', k ', k)
            
        M,N = X_train.shape
        
        solution = self.train(X_train, Y_train, c)
        W = np.array(solution['x'][0:N])
        bias = solution['x'][N]
        print('BIAS :', bias)
            
        N_train, D_train = X_train.shape
        error_train = self.score(W, X_train, Y_train, bias)
        accuracy_train = (1 - error_train/N_train)*100
        print('ACCURACY ON TRAINING DATA : ', accuracy_train)
            
        N_val, D_val = X_val.shape
        error_val = self.score(W, X_val, Y_val, bias)
        accuracy_val = (1 - error_val/N_val)*100
        print('ACCURACY ON VALIDATION DATA : ', accuracy_val)
            
        N_test, D_test = X_test.shape
        error_test = self.score(W, X_test, Y_test, bias)
        accuracy_test = (1 - error_test/N_test)*100
        print('ACCURACY ON TEST DATA : ', accuracy_test)
        
        return (accuracy_train, accuracy_val, accuracy_test)

###############################################################################
############################ PCA IMPLEMENTATION ###############################
###############################################################################

def prepare_data(data):    
    M,N = data.shape
    X = data[:, 0:N-1]
    Y = data[:, N-1]
    Y = Y.reshape(M,1)
    return (X, Y)

def normalize(X):    
    M,N = X.shape    
    X_mean = X.sum(axis=0)/M
    X_sd = np.sqrt( ((X - X_mean)**2).sum(axis=0)/M )    
    return (((X - X_mean) / X_sd), X_mean, X_sd)

def rescale(X, X_mean, X_sd):
    return (X - X_mean)/ X_sd

def PCA(X_train, Y_train, X_val, Y_val, X_test, Y_test, k, accuracy_train, accuracy_val, accuracy_test):      
    # 1. Normalize the data
    (X_train, X_mean, X_sd) = normalize(X_train)
    
    # 2. Construct covariance matrix
    covariance_matrix = np.dot(X_train.transpose(), X_train)
    
    # 3. Select k eigen vectors corresponding to the largest eigen values
    eigen_values, eigen_vectors = np.linalg.eig(covariance_matrix)
    idx = eigen_values.argsort()[::-1][0:k]
    U = eigen_vectors[:, idx]
    
    # 4. Project normalized data onto these eigenvectors
    X_train_proj = np.dot(X_train, U)
    
    # 5. Fit SVM using the normalized data    
    # 6. Normalize test set using mean and standard deviation
    # 7. Project it onto k selected eigen vectors 
    # 8. Use the new test set for prediction and compare
    X_val = rescale(X_val, X_mean, X_sd)
    X_test = rescale(X_test, X_mean, X_sd)
    
    X_val_proj = np.dot(X_val, U)
    X_test_proj = np.dot(X_test, U)
       
    svm = SVM()
    for i in range(0,4):
        print('---------------------------------------------------------------------------')
        c = 10**i        
        (train_acc, val_acc, test_acc) = svm.fit_svm(X_train_proj, Y_train, X_val_proj, Y_val, X_test_proj, Y_test, k, c)
        accuracy_train[k-1][i] = train_acc
        accuracy_val[k-1][i] = val_acc
        accuracy_test[k-1][i] = test_acc   
    
    return (accuracy_train, accuracy_val, accuracy_test)

def SvmPca(K, C):
    (X_train, Y_train) = prepare_data(data_train)
    (X_val, Y_val) = prepare_data(data_val)
    (X_test, Y_test) = prepare_data(data_test)
    
    accuracy_train = np.empty((K, C))
    accuracy_val = np.empty((K, C))
    accuracy_test = np.empty((K, C))
    
    for k in range(1, K+1):
        (accuracy_train, accuracy_val, accuracy_test) = PCA(X_train, Y_train, X_val, Y_val, X_test, Y_test, k, accuracy_train, accuracy_val, accuracy_test)
        
    return (accuracy_train, accuracy_val, accuracy_test)

(accuracy_train, accuracy_val, accuracy_test) = SvmPca(12, 4)     
errors_train = 100 - accuracy_train
errors_val = 100 - accuracy_val
errors_test = 100 - accuracy_test
    