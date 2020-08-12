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

cvxopt.solvers.options['maxiters'] = 1000

def prepare_data(data):    
    X = data[:, 0:57]
    Y = data[:, 57]
    NUM, DIM = X.shape
    Y = Y.reshape(NUM,1)
    #X = np.concatenate((X, np.ones((NUM,1))), axis=1)
    return (X, Y)

def kernel(X1, X2, sigma2):
    return math.exp(-1.* np.sum((X1-X2)**2)/ (sigma2))

def computeP(NUM, X, Y, sigma2):
    P = np.zeros((NUM, NUM))
    for i in range(NUM):
        for j in range(NUM):
            P[i][j] = kernel(X[i], X[j], 2*(sigma2))*(Y[i]*Y[j])
    return P

def train(X, Y, c, sigma):
    NUM, DIM = X.shape         
        
    P = cvxopt.matrix(computeP(NUM, X, Y, sigma))
    print('COMPUTED P')
    q = cvxopt.matrix(-1.*np.ones((NUM,1)))
    
    G = cvxopt.matrix(np.concatenate((-1*np.eye(NUM), np.eye(NUM)), axis = 0))
    h = cvxopt.matrix(np.concatenate((np.zeros((NUM,1)), c*np.ones((NUM,1))), axis = 0))
    
    A = cvxopt.matrix(Y.T)
    b = cvxopt.matrix(np.zeros(1))
    
    return cvxopt.solvers.qp(P, q, G, h, A, b)

def pred(X_query, X_train, lagranges, Y_train, sigma2):
    T_NUM, T_DIM = X_train.shape
    prediction = 0
    for j in range(T_NUM):
            prediction = prediction + lagranges[j]*Y_train[j]*kernel(X_query, X_train[j], 2*(sigma2))            
    return prediction

def accuracy(lagranges, X, Y, X_train, Y_train, sigma2, bias):
    D_NUM, D_DIM = X.shape
    T_NUM, T_DIM = X_train.shape
    predictions = []
    for i in range(D_NUM):
        X_query = X[i]
        prediction = 0
        for j in range(T_NUM):
            prediction = prediction + lagranges[j]*Y_train[j]*kernel(X_query, X_train[j], 2*(sigma2))
        predictions.append(prediction + bias)
    predictions = np.array(predictions).reshape(D_NUM,1)*Y
    predictions[predictions>=0] = 0
    predictions[predictions<0] = 1
    return np.sum(predictions)

def compute_bias(lagranges, X_train, Y_train, sigma2):
    L_NUM, L_DIM = lagranges.shape
    support_vectors = bias = 0
    for i in range(L_NUM):
        #SUPPORT VECTOR
        if lagranges[i][0] > 0:
            support_vectors = support_vectors+1
            bias = bias + ( Y_train[i] - pred(X_train[i], X_train, lagranges, Y_train, sigma2) )
    print('SUPPORT VECTORS ', support_vectors)
    return (bias/support_vectors)
    

def fit_best_svm():
    best_c = c = best_sigma = 1
    best_solution = None
    best_bias = 1
    min_error_train = min_error_val = 3000
    X_train, Y_train = prepare_data(data_train)
    X_val, Y_val = prepare_data(data_val)
    X_test, Y_test = prepare_data(data_test)
    
    for i in range(8,9):
        c = 10**i
        for j in range(3,4):
            sigma2 = 10**j            
        
            print('CALCULATING SVM SOLUTION FOR c and sigma ', c, sigma2)
            
            solution = train(X_train, Y_train, c, sigma2)
            lagranges = np.array(solution['x']).reshape(-1,1)
            lagranges[lagranges<1e-4] = 0
            
            print('COMPUTING B')
            bias = compute_bias(lagranges, X_train, Y_train, sigma2)
            print('BIAS ', bias)
            
            print('CACULATING ERROR')
            N_train, D_train = X_train.shape
            error_train = accuracy(lagranges, X_train, Y_train, X_train, Y_train, sigma2, bias)
            print('ERROR ON TRAINING DATA : ', (1 - error_train/N_train)*100)
            
            N_val, D_val = X_val.shape
            error_val = accuracy(lagranges, X_val, Y_val, X_train, Y_train, sigma2, bias)
            print('ERROR ON VALIDATION DATA : ', (1 - error_val/N_val)*100)
            
            N_test, D_test = X_test.shape
            error_test = accuracy(lagranges, X_test, Y_test, X_train, Y_train, sigma2, bias)
            print('ERROR ON TEST DATA : ', (1 - error_test/N_train)*100)
            
            if error_val <= min_error_val and error_train <= min_error_train:
                best_c = c
                best_sigma = sigma2
                best_bias = bias
                best_solution = solution
                min_error_val = error_val
                min_error_train = error_train            
            
            print('---------------------------------------------------------------------------------------')
    
    lagranges = np.array(best_solution['x']).reshape(-1,1)
    
    error_test = accuracy(lagranges, X_test, Y_test, X_train, Y_train, best_sigma, best_bias)
    
    print('BEST C OBTAINED ', best_c)
    print('BEST SIGMA OBTAINED ', best_sigma)
    print('TEST ERROR ON DATA SET : ', error_test)    
        
    return (best_solution, best_c, best_sigma)

best_solution, best_c, best_sigma = fit_best_svm()