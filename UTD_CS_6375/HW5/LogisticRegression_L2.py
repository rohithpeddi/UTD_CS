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

def probabilities(W, bias, X):
    functional_margin = np.dot(X,W) + bias
    e = np.exp(-1*functional_margin)
    P_x_y_1 = (1/(1+e))
    P_x_y_m1 = (e/(1+e))
    return (P_x_y_1, P_x_y_m1, functional_margin)

def gradients(W, X, bias, Y, lamb):
    M,N = X.shape
    P_x_y_1, P_x_y_m1, functional_margin = probabilities(W, bias, X)
    G_b = ((0.5*(Y+1))-P_x_y_1).sum()
    G_w = np.sum(X*((0.5*(Y+1))-P_x_y_1), axis=0).reshape(N,1) - lamb*W
    likelihood = np.sum( 0.5*(Y+1)*functional_margin - np.log(1 + np.exp(functional_margin)), axis=0) - (lamb)*np.sum(W**2,axis=0)
    return (G_b, G_w, likelihood)

def calculate_loss(W, Y, X, bias):
    return np.sum((0.5)*(Y+1)*(np.dot(X, W)+bias) - np.log(1 + np.exp(np.dot(X,W) + bias)))

def logistic_train(X, Y, alpha, lamb):
    M, N = X.shape
    W = np.ones(N).reshape(N,1)*(0.5)
    bias = 0.5
    iterations = 0
    #print('PRINTING ACCURACY AFTER EACH ITERATION ')
    (G_b, G_w, likelihood) = gradients(W, X, bias, Y, lamb)
    current_likelihood = previous_likelihood = likelihood
    while True : 
        previous_likelihood = current_likelihood
        W = W + alpha * G_w
        bias = bias + alpha * G_b
        iterations = iterations + 1
        (G_b, G_w, current_likelihood) = gradients(W, X, bias, Y, lamb)
        if iterations%1000 == 0:
            print(iterations, G_b, accuracy(X, Y, W, bias), current_likelihood-previous_likelihood, current_likelihood, previous_likelihood)
        if abs(current_likelihood-previous_likelihood) < 1e-4:
            break
        #print(G_b, accuracy(X, Y, W, bias), current_likelihood-previous_likelihood)
        
    return (W, bias, iterations)

def accuracy(X, Y, W, bias):
    M,N = X.shape
    Y_pred = np.dot(X, W) + bias
    Y_pred[Y_pred>0] = 1
    Y_pred[Y_pred<0] = -1
    misclassifications =  np.sum(abs(Y-Y_pred))/2
    return (1- misclassifications/M)*100

def logistic_validate(X_train, Y_train, X_val, Y_val, X_test, Y_test):
    best_W = best_bias = best_alpha = best_lamb = None
    best_accuracy = 0
    for i in range(-6, -5):        
        alpha = 10**i
        for j in range(-4,5):
            lamb = 10**j
            print('------------------------------------------------------------')
            print('VALIDATION FOR alpha ', alpha, ', lambda ', lamb)
            (W, bias, iterations) = logistic_train(X_train, Y_train, alpha, lamb)
            training_accuracy = accuracy(X_train, Y_train, W, bias)  
            current_accuracy = accuracy(X_val, Y_val, W, bias)
            test_accuracy = accuracy(X_test, Y_test, W, bias)
            print('------------------------------------------------------------')
            print('------------------------------------------------------------')
            print('TRAINING ACCURACY ', training_accuracy)
            print('VALIDATION ACCURACY ', current_accuracy)            
            print('TEST ACCURACY ', test_accuracy)
            print('FOUND BEST W and bias in ', iterations, ' iterations')
            print('------------------------------------------------------------')
            print('------------------------------------------------------------')
            if current_accuracy > best_accuracy :
                best_accuracy = current_accuracy
                best_W = W
                best_bias = bias     
                best_alpha = alpha
                best_lamb = lamb
            print('------------------------------------------------------------')
        
        
    return (best_W, best_bias, best_alpha, best_lamb)

(X_train, Y_train) = prepare_data(data_train)
(X_val, Y_val) = prepare_data(data_val)
(X_test, Y_test) = prepare_data(data_test)

(W, bias, alpha, lamb) = logistic_validate(X_train, Y_train, X_val, Y_val, X_test, Y_test)
training_accuracy = accuracy(X_train, Y_train, W, bias)
print('ACCURACY ON TRAINING SET ', training_accuracy)
test_accuracy = accuracy(X_test, Y_test, W, bias)
print('ACCURACY ON TEST SET ', test_accuracy)

    
    
    