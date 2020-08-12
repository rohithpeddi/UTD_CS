# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 10:06:02 2020

@author: ROHITH PEDDI
"""

#RESCALE TEST DATA POINTS BEFORE CALCULATING

import pandas as pd
import numpy as np

data_train = pd.read_csv("spam_train.data").values
data_val = pd.read_csv("spam_validation.data").values
data_test = pd.read_csv("spam_test.data").values

def prepare_data(data):    
    X = data[:, 0:57]
    Y = data[:, 57]
    NUM, DIM = X.shape
    Y = Y.reshape(NUM,1)
    return (X, Y)

def normalize(X):    
    NUM, DIM = X.shape    
    X_mean = X.sum(axis=0)/NUM
    X_sd = np.sqrt( ((X - X_mean)**2).sum(axis=0)/NUM )    
    return (((X - X_mean) / X_sd), X_mean, X_sd)

def rescale(X_point, X_mean, X_sd):
    return ((X_point - X_mean) / X_sd)

def distance(X, X_query):
    return ((X - X_query)**2).sum(axis = 1)

def predict(X, X_query, k, Y):
    dist = distance(X, X_query)
    idx = np.argpartition(dist, k) 
    return 1 if (np.sum(Y[idx[:k]]) > (k/2.0)) else 0

def prediction_error(Y_pred, Y):
    return np.sum(abs(np.array(Y_pred).reshape(-1, 1) - Y))

def kNN(X_train, Y_train, X_val, Y_val, X_test, Y_test):
    V_NUM, V_DIM = X_val.shape
    T_NUM, T_DIM = X_test.shape
    
    (X_norm, X_mean, X_sd) = normalize(X_train)
    
    best_k = 1
    min_error = 800 * 1.
    for k in [1,5,11,15,21]:        
        Y_pred = []
        for i in range(0,V_NUM):
            Y_pred.append(predict(X_norm, rescale(X_val[i], X_mean, X_sd), k, Y_train))   
            
        validation_error = prediction_error(Y_pred, Y_val)        
        print('VALIDATION ERROR IN USING k', k, 1- (validation_error/V_NUM))
        validation_error = 1- (validation_error/V_NUM)
        
        Y_pred = []
        for i in range(0,T_NUM):
            Y_pred.append(predict(X_norm, rescale(X_test[i], X_mean, X_sd), k, Y_train))        
        
        test_error = prediction_error(Y_pred, Y_test)        
        print('TEST ERROR IN USING k', k, 1- (test_error/T_NUM))        
        if validation_error < min_error :
            min_error = validation_error
            best_k = k
    
    return (best_k, min_error)

(X_train, Y_train) = prepare_data(data_train)
(X_test, Y_test) = prepare_data(data_test)
(X_val, Y_val) = prepare_data(data_val)

(best_k, min_error) = kNN(X_train, Y_train, X_val, Y_val, X_test, Y_test)
print('FOUND BEST k WITH ERROR ', best_k, min_error)

