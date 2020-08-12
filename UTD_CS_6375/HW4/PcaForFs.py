# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 20:45:10 2020

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
        
class PCAForFS(object):
    
    def __init__(self, data_train, data_val, data_test):
        self.data_train = data_train
        self.data_val = data_val
        self.data_test = data_test
        self.X_train = None
        self.Y_train = None
        self.X_val = None
        self.Y_val = None
        self.X_test = None
        self.Y_test = None
        self.covariance_matrix = None
        self.eigen_values = None
        self.eigen_vectors = None
        self.probability_dist = None
        self.X_mean = None
        self.X_sd = None
        
        self.preprocess_data()
        
    def prepare_data(self, data):    
        M,N = data.shape
        X = data[:, 0:N-1]
        Y = data[:, N-1]
        Y = Y.reshape(M,1)
        return (X, Y)
    
    def normalize(self, X):    
        M,N = X.shape    
        X_mean = X.sum(axis=0)/M
        X_sd = np.sqrt( ((X - X_mean)**2).sum(axis=0)/M )    
        return (((X - X_mean) / X_sd), X_mean, X_sd)
    
    def rescale(self, X, X_mean, X_sd):
        return (X - X_mean)/ X_sd
        
    def preprocess_data(self):
        (X_train, Y_train) = self.prepare_data(data_train)
        (X_val, Y_val) = self.prepare_data(data_val)
        (X_test, Y_test) = self.prepare_data(data_test)
        
        (X_train, X_mean, X_sd) = self.normalize(X_train)
        X_val = self.rescale(X_val, X_mean, X_sd)
        X_test = self.rescale(X_test, X_mean, X_sd)
        
        covariance_matrix = np.dot(X_train.transpose(), X_train)
        eigen_values, eigen_vectors = np.linalg.eig(covariance_matrix) 
        
        self.X_train = X_train
        self.Y_train = Y_train
        self.X_val = X_val
        self.Y_val = Y_val
        self.X_test = X_test
        self.Y_test = Y_test
        
        self.X_mean = X_mean
        self.X_sd = X_sd
        
        self.covariance_matrix = covariance_matrix
        self.eigen_values = eigen_values
        self.eigen_vectors = eigen_vectors
    
    def PCA(self, K, S):          
        svm = SVM()  
           
        accuracies_train = np.empty((K, S))
        accuracies_val = np.empty((K, S))
        accuracies_test = np.empty((K, S))
        
        M, N = self.X_train.shape
        
        for k in range(1, K+1):
            # 1. For each k fetch the top k eigen values and corresponding eigen vectors
            idx = self.eigen_values.argsort()[::-1][0:k]
            U = self.eigen_vectors[:, idx]
            
            # 2. Generate a probability distribution corresponding to eigen vectors selected
            self.probability_dist = (1/k)*np.sum(U**2, axis = 1)
            
            for s in range(1, S+1):              
                avg_accuracy_train = avg_accuracy_val = avg_accuracy_test = 0
                for e in range(0, 100):
                    # 3. Sample s features from the training dataset from weighted distribution of features                                        
                    
                    idx_sampled = np.random.choice(list(range(N)), s, p = self.probability_dist)
                    X_train_sampled = self.X_train[:, idx_sampled]
                    X_val_sampled = self.X_val[:, idx_sampled]
                    X_test_sampled = self.X_test[:, idx_sampled]                    
                    
                    # 4. Fit SVM for k and s combination by finding best c using validation dataset
                    best_c = best_accuracy_train = best_accuracy_test = best_accuracy_val = None
                    max_val_accuracy = 0
                    for i in range(0,4):
                        print('-----------------------------------------------------------------------------')
                        c = 10**i
                        (accuracy_train, accuracy_val, accuracy_test) = svm.fit_svm(X_train_sampled, self.Y_train, X_val_sampled, self.Y_val, X_test_sampled, self.Y_test, k, c)
                        if max_val_accuracy < accuracy_val:
                            best_accuracy_val = max_val_accuracy = accuracy_val
                            best_accuracy_train = accuracy_train
                            best_accuracy_test = accuracy_test
                            best_c = c                
                    avg_accuracy_train = avg_accuracy_train + best_accuracy_train
                    avg_accuracy_val = avg_accuracy_val + best_accuracy_val
                    avg_accuracy_test = avg_accuracy_test + best_accuracy_test
                
                accuracies_train[k-1][s-1] = (avg_accuracy_train/100)
                accuracies_val[k-1][s-1] = (avg_accuracy_val/100)
                accuracies_test[k-1][s-1] = (avg_accuracy_test/100)
                
            
        return (accuracies_train, accuracies_val, accuracies_test)
    
pcaForFs = PCAForFS(data_train, data_val, data_test)
(accuracies_train, accuracies_val, accuracies_test) = pcaForFs.PCA(10, 20)