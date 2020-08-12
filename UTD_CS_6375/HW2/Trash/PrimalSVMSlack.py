#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 00:40:43 2020

@author: rohith
"""
import pandas as pd
import numpy as np
import cvxopt as cvxopt

data_train = pd.read_csv("spam_train.data").values
data_val = pd.read_csv("spam_validation.data").values
data_test = pd.read_csv("spam_test.data").values

data_train[data_train[:, 57] == 0, 57] = -1
data_val[data_val[:, 57] == 0, 57] = -1
data_test[data_test[:, 57] == 0, 57] = -1

def prepare_data(data):    
    X = data[:, 0:57]
    Y = data[:, 57]
    NUM, DIM = X.shape
    Y = Y.reshape(NUM,1)
    X = np.concatenate((X, np.ones((NUM,1))), axis=1)
    return (X, Y)

def train(X, Y, c):
    NUM, DIM = X.shape    
    P = cvxopt.matrix(np.concatenate((np.eye(NUM+DIM, M=DIM).T, np.zeros((NUM,NUM+DIM))), axis = 0))
    q = cvxopt.matrix(np.concatenate((np.zeros((DIM,1)),c*np.ones((NUM,1))), axis=0))
    
    G_u = np.concatenate((-1.*X*Y, -1.*np.eye(NUM)), axis = 1)
    G_l = np.concatenate((np.zeros((NUM,DIM)), -1.*np.eye(NUM)), axis = 1)    
    
    G = cvxopt.matrix(np.concatenate((G_u, G_l), axis=0))    
    h = cvxopt.matrix(np.concatenate((-1.*np.ones((NUM, 1)), np.zeros((NUM,1))), axis=0))    
    return cvxopt.solvers.qp(P, q, G, h)

def score(W, X, Y):    
    pred = np.dot(X, W) * Y
    pred[pred>=0] = 0
    pred[pred<0] = 1
    return np.sum(pred)

def fit_best_svm():
    best_c = c = 1
    best_solution = None
    min_error_train = min_error_val = 3000
    X_train, Y_train = prepare_data(data_train)
    X_val, Y_val = prepare_data(data_val)
    
    for i in range(2,3):
        c = 10**i
        
        print('CALCULATING SVM SOLUTION FOR c ', c)
        
        solution = train(X_train, Y_train, c)
        W = np.array(solution['x'][0:58])
        
        error_train = score(W, X_train, Y_train)
        print('ERROR ON TRAINING DATA : ', error_train)
        
        error_val = score(W, X_val, Y_val)
        print('ERROR ON VALIDATION DATA : ', error_val)
        
        if error_val <= min_error_val and error_train <= min_error_train:
            best_c = c
            best_solution = solution
            min_error_val = error_val
            min_error_train = error_train
        
        print('---------------------------------------------------------------------------------------')
    
    
    X_test, Y_test = prepare_data(data_test)
    W = np.array(best_solution['x'][0:58])
    error_test = score(W, X_test, Y_test)
    
    print('BEST C OBTAINED ', best_c)
    print('TEST ERROR ON DATA SET : ', error_test)    
        
    return (best_solution, best_c)

best_solution, best_c = fit_best_svm()
    
    
    
    
    
    
    
    
    
    
    
