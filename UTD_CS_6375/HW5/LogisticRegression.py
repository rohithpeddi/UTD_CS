# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 21:37:54 2020

@author: ROHITH PEDDI
"""

import pandas as pd
import numpy as np

data_train = pd.read_csv('sonar_train.data', header = None).values
data_val = pd.read_csv('sonar_valid.data', header = None).values
data_test = pd.read_csv('sonar_test.data', header = None).values

M, N = data_train.shape

data_train[data_train[:, N-1] == 2, N-1] = -1
data_val[data_val[:, N-1] == 2, N-1] = -1
data_test[data_test[:, N-1] == 2, N-1] = -1

def prepare_data(data):    
    M,N = data.shape
    X = data[:, 0:N-1]
    Y = data[:, N-1]
    Y = Y.reshape(M,1)
    return (X, Y)

def normalize(X):    
    NUM, DIM = X.shape    
    X_mean = X.sum(axis=0)/NUM
    X_sd = np.sqrt( ((X - X_mean)**2).sum(axis=0)/NUM )    
    return (((X - X_mean) / X_sd), X_mean, X_sd)

def rescale(X, X_mean, X_sd):
    return (X - X_mean) / X_sd

def probabilities_bak(W, bias, X):
    functional_margin = np.dot(X,W) + bias
    e = np.exp(-1*functional_margin)
    P_x_y_1 = (1/(1+e))
    P_x_y_m1 = (e/(1+e))
    return (P_x_y_1, P_x_y_m1, functional_margin)

def probabilities(W, bias, X):
    functional_margin = np.dot(X,W) + bias
    e = np.exp(functional_margin)
    P_x_y_1 = (e/(1+e))
    P_x_y_m1 = (1/(1+e))
    return (P_x_y_1, P_x_y_m1, functional_margin)

def gradients(W, X, bias, Y):
    M,N = X.shape
    P_x_y_1, P_x_y_m1, functional_margin = probabilities(W, bias, X)
    G_b = ((0.5*(Y+1))-P_x_y_1).sum()
    G_w = np.sum(X*((0.5*(Y+1))-P_x_y_1), axis=0).reshape(N,1)
    likelihood = np.sum( 0.5*(Y+1)*functional_margin - np.log(1 + np.exp(functional_margin)), axis=0)
    return (G_b, G_w, likelihood)

def logistic_train(X, Y, alpha):
    M, N = X.shape
    W = np.ones(N).reshape(N,1)*(0.25)
    bias = 0.75
    iterations = 0
    print('PRINTING ACCURACY AFTER EACH ITERATION ')
    (G_b, G_w, likelihood) = gradients(W, X, bias, Y)
    current_likelihood = previous_likelihood = likelihood
    while True : 
        #step = 2.0/(2.0 + iterations)
        step = alpha
        previous_likelihood = current_likelihood
        W = W + step * G_w
        bias = bias + step * G_b
        iterations = iterations + 1
        (G_b, G_w, current_likelihood) = gradients(W, X, bias, Y)
        if iterations%10000 == 0:
            print(iterations, G_b, accuracy(X, Y, W, bias), current_likelihood-previous_likelihood, current_likelihood, previous_likelihood)
        
        if abs(current_likelihood-previous_likelihood) < 1e-7:
            break
        #print(G_b, accuracy(X, Y, W, bias), current_likelihood-previous_likelihood, current_likelihood, previous_likelihood)
        
    return (W, bias, iterations)

def accuracy(X, Y, W, bias):
    M,N = X.shape
    Y_pred = np.dot(X, W) + bias
    Y_pred[Y_pred>=0] = 1
    Y_pred[Y_pred<0] = -1
    misclassifications =  np.sum(abs(Y-Y_pred))/2
    return (1- misclassifications/M)*100

def logistic_validate(X_train, Y_train, X_val, Y_val):
    best_W = best_bias = best_alpha = None
    best_accuracy = 0
    for i in range(-5, -3):
        print('------------------------------------------------------------')
        alpha = 10**i
        print('VALIDATION FOR alpha ', alpha)
        (W, bias, iterations) = logistic_train(X_train, Y_train, alpha)
        training_accuracy = accuracy(X_train, Y_train, W, bias)  
        current_accuracy = accuracy(X_val, Y_val, W, bias)
        test_accuracy = accuracy(X_test, Y_test, W, bias)
        print('------------------------------------------------------------')
        print('------------------------------------------------------------')
        print('TRAINING ACCURACY ', training_accuracy)
        print('VALIDATION ACCURACY ', current_accuracy)            
        print('TEST ACCURACY ', test_accuracy)
        print('W and bias in ', iterations, ' iterations')
        print('------------------------------------------------------------')
        print('------------------------------------------------------------')
        if current_accuracy > best_accuracy :
            best_accuracy = current_accuracy
            best_W = W
            best_bias = bias     
            best_alpha = alpha
        
        print('------------------------------------------------------------')
        
    return (best_W, best_bias, best_alpha)

(X_train, Y_train) = prepare_data(data_train)
#(X_scaled_train, X_mean, X_sd) = normalize(X_train)
(X_val, Y_val) = prepare_data(data_val)
#X_val = rescale(X_val, X_mean, X_sd)
(X_test, Y_test) = prepare_data(data_test)
#X_test = rescale(X_test, X_mean, X_sd)

(W, bias, alpha) = logistic_validate(X_train, Y_train, X_val, Y_val)
training_accuracy = accuracy(X_train, Y_train, W, bias)
print('ACCURACY ON TRAINING SET ', training_accuracy)
test_accuracy = accuracy(X_test, Y_test, W, bias)
print('ACCURACY ON TEST SET ', test_accuracy)

    
    
    