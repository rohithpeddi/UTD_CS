# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 12:00:08 2020

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

################################################################################
################################# SVM IMPLEMENTATION ###########################
################################################################################

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
    
    def prepare_data(self, data):    
        M,N = data.shape
        X = data[:, 0:N-1]
        Y = data[:, N-1]
        Y = Y.reshape(M,1)
        return (X, Y)
    
    def fit_svm(self, data_train, data_val, data_test):
        (X_train, Y_train) = self.prepare_data(data_train)
        (X_val, Y_val) = self.prepare_data(data_val)
        (X_test, Y_test) = self.prepare_data(data_test)
                        
        best_c = best_accuracy_train = best_accuracy_val = best_accuracy_test = None
        max_validation_accuracy = 0
        for i in range(0, 4):     
            print('------------------------------------------------------------')
            c = 10**i
            print('CALCULATING SVM SOLUTION FOR c ', c)                
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
            
            if max_validation_accuracy < accuracy_val:
                best_accuracy_val = max_validation_accuracy = accuracy_val
                best_accuracy_train = accuracy_train
                best_accuracy_test = accuracy_test
                best_c = c
                
            
        return (best_c, best_accuracy_train, best_accuracy_val, best_accuracy_test)
    
svm = SVM()
(best_c, accuracy_train, accuracy_val, accuracy_test) = svm.fit_svm(data_train, data_val, data_test)
    
