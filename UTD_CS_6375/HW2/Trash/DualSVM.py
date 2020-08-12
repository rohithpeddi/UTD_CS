# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 10:05:39 2020

@author: ROHITH PEDDI
"""
import pandas as pd
import numpy as np
import math
import cvxopt as cvxopt

data_train = pd.read_csv("spam_train.data").values
data_val = pd.read_csv("spam_validation.data").values
data_test = pd.read_csv("spam_test.data").values

data_train[data_train[:, 57] == 0, 57] = -1
data_val[data_val[:, 57] == 0, 57] = -1
data_test[data_test[:, 57] == 0, 57] = -1

### CHANGE THE KERNEL FUNCTION
### CHANGE THE CLASSIFIER
### ADD AN EASILY COMPUTABLE KERNEL

def prepare_data(data):    
    X = data[:, 0:57]
    Y = data[:, 57]
    NUM, DIM = X.shape
    Y = Y.reshape(NUM,1)
    X = np.concatenate((X, np.ones((NUM,1))), axis=1)
    return (X, Y)

#def guassianKernel(x, z, sigma, DIM):
#    dist = 0
#    for i in range(DIM):
#        dist = dist + (x[i]-z[i])**2
#        
#    k = (-1. * dist)/(2*(sigma**2))
#    k = math.exp(k)
#    return k

def kernel(X1, X2, sigma2):
    return math.exp(-1.* np.sum((X1-X2)**2)/ (2* (sigma2)))

def computeP(NUM, DIM, X, Y, sigma):
    P = np.zeros((NUM, NUM))
    for i in range(NUM):
        for j in range(NUM):
            P[i][j] = kernel(X[i], X[j], sigma**2)*(Y[i]*Y[j])
    return P

def train(X, Y, c, sigma):
    NUM, DIM = X.shape         
    
#    Cross = -2.* np.dot(X, X.T)
#    X_sum = np.sum((X**2), axis=1).reshape(-1,1)    
#    P_mat = np.dot(X_sum, np.ones((1, NUM))) + X_sum
#    P_mat = abs(P_mat + Cross)
#    P_mat = -1. * P_mat / (2* (sigma**2))
#    P_mat = np.exp(P_mat)
#    P_mat = np.dot(Y, Y.T) * P_mat
#    
#    P = cvxopt.matrix(computeP(NUM, DIM, X, Y, sigma))
#    #P = cvxopt.matrix(P_mat)
#    print('COMPUTED P')
#    q = cvxopt.matrix(-1.*np.ones((NUM,1)))
#    
#    G = cvxopt.matrix(np.concatenate((-1*np.eye(NUM), np.eye(NUM)), axis = 0))
#    h = cvxopt.matrix(np.concatenate((np.zeros((NUM,1)), c*np.ones((NUM,1))), axis = 0))
#    
#    A = cvxopt.matrix(Y.T)
#    b = cvxopt.matrix(np.zeros(1))   
    
    P = cvxopt.matrix(computeP(NUM, DIM, X, Y, sigma))
    print('COMPUTED P')
    h = cvxopt.matrix(np.concatenate((np.zeros((NUM,1)), c*np.ones((NUM,1))), axis = 0))
    
    return cvxopt.solvers.qp(P, q, G, h, A, b)

def score(W, X, Y):    
    pred = np.dot(X, W) * Y
    pred[pred>=0] = 0
    pred[pred<0] = 1
    return np.sum(pred)

def computeAccuracy(data, w, b):#Given data, w and b computeAccuracy calculates accuracy
    x, y = prepare_data(data)
    length = len(data)
    count = 0
    for i in range(length):
        f = np.dot(w, x[i]) + b
        if f * y[i] > 0:
            count += 1
    accuracy = count/length * 100
    return accuracy

def fit_best_svm():
    best_c = c = best_sigma = 1
    best_solution = None
    min_error_train = min_error_val = 3000
    X_train, Y_train = prepare_data(data_train)
    X_val, Y_val = prepare_data(data_val)
    
    finalWeight = []
    finalBias = 0
    bestAccuracy = 0
    
    for i in range(0,9):
        c = 10**i
        for j in range(-1,4):
            sigma = 10**j            
        
            print('CALCULATING SVM SOLUTION FOR c and sigma ', c, sigma)
            
            solution = train(X_train, Y_train, c, sigma)
            lst = np.array(solution['x'])
            
#            error_train = accuracy(lagrange_multipliers, X_train, Y_train)
#            print('ERROR ON TRAINING DATA : ', error_train)
#            
#            error_val = score(lagrange_multipliers, X_val, Y_val)
#            print('ERROR ON VALIDATION DATA : ', error_val)
#            
#            if error_val <= min_error_val and error_train <= min_error_train:
#                best_c = c
#                best_sigma = sigma
#                best_solution = solution
#                min_error_val = error_val
#                min_error_train = error_train
            
            n = DIM
            m = NUM
            #Calculate Weight
            weight = []
            for k1 in range(n):
                k = 0
                for k2 in range(m):
                    k = k + lst[k2]*Y_train[k2]*X_train[k2][k1]
                    break
                weight.append(k)
            
            weight = np.array(weight).reshape(58,1)
            
            #Calculate bias(Intercept) using Complementary Slackness
            supportVectorsCount = 0
            bias = 0
            for k3 in range(m):
                if(lst[k3] > 0):
                    supportVectorsCount = supportVectorsCount + 1
                    bias = bias + (Y_train[k3] - np.dot(weight, X_train[k3]))
            #print(supportVectorsCount)
            bias = bias/supportVectorsCount
            acc = computeAccuracy(data_train, weight, bias)
            print('Accuracy on Training data set is',acc,' for value of C =',c,'and sigma =',sigma)
            acc = computeAccuracy(data_val, weight, bias)
            print('Accuracy on Validation data set is',acc,' for value of C =',c,'and sigma =',sigma)
            if acc > bestAccuracy:
                best_c = c
                best_sigma = sigma
                finalWeight = weight
                finalBias = bias
                bestAccuracy = acc
            
            
            print('---------------------------------------------------------------------------------------')
    
    
    X_test, Y_test = prepare_data(data_test)
    lagrange_multipliers = np.array(best_solution['x']).reshape(-1,1)
    W = (lagrange_multipliers*Y_train*X_train).sum(axis = 0).reshape(-1,1)
    error_test = score(W, X_test, Y_test)
    
    print('BEST C OBTAINED ', best_c)
    print('BEST SIGMA OBTAINED ', best_sigma)
    print('TEST ERROR ON DATA SET : ', error_test)    
        
    return (best_solution, best_c, best_sigma)


X, Y = prepare_data(data_train)
NUM, DIM = X.shape

sigma = 0.1
c =1
print('STARTED COMPUTATION OF P')
#P = cvxopt.matrix(computeP(NUM, DIM, X, Y, sigma))
#P = cvxopt.matrix(P_mat)
print('COMPUTED P')
q = cvxopt.matrix(-1.*np.ones((NUM,1)))

G = cvxopt.matrix(np.concatenate((-1*np.eye(NUM), np.eye(NUM)), axis = 0))
#h = cvxopt.matrix(np.concatenate((np.zeros((NUM,1)), c*np.ones((NUM,1))), axis = 0))

A = cvxopt.matrix(Y.T)
b = cvxopt.matrix(np.zeros(1))   

best_solution, best_c, best_sigma = fit_best_svm()