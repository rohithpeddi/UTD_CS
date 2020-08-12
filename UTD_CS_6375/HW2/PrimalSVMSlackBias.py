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
    #X = np.concatenate((X, np.ones((NUM,1))), axis=1)
    return (X, Y)

def train(X, Y, c):
    NUM, DIM = X.shape    
    P = cvxopt.matrix(np.concatenate((np.eye(NUM+DIM+1, M=DIM).T, np.zeros((NUM+1,NUM+DIM+1))), axis = 0))
    q = cvxopt.matrix(np.concatenate((np.concatenate((np.zeros((DIM,1)),c*np.ones((NUM,1))), axis=0), np.zeros((1,1))), axis = 0))
    
    G_u = np.concatenate((-1.*X*Y, -1.*np.eye(NUM)), axis = 1)
    G_l = np.concatenate((np.zeros((NUM,DIM)), -1.*np.eye(NUM)), axis = 1)    
    G_b = np.concatenate((-1.* Y, np.zeros((NUM,1))), axis = 0)
    
    G_com = np.concatenate((G_u, G_l), axis=0)
    
    G = cvxopt.matrix(np.concatenate((G_com, G_b), axis=1))    
    h = cvxopt.matrix(np.concatenate((-1.*np.ones((NUM, 1)), np.zeros((NUM,1))), axis=0))    
    return cvxopt.solvers.qp(P, q, G, h)

def score(W, X, Y, bias):    
    pred = (np.dot(X, W) + bias) * Y 
    pred[pred>=0] = 0
    pred[pred<0] = 1
    return np.sum(pred)

def fit_best_svm():
    best_c = c = 1
    best_solution = None
    min_error_train = min_error_val = 3000
    X_train, Y_train = prepare_data(data_train)
    X_val, Y_val = prepare_data(data_val)
    X_test, Y_test = prepare_data(data_test)
    
    for i in range(0,9):
        c = 10**i
        
        print('CALCULATING SVM SOLUTION FOR c ', c)
        
        solution = train(X_train, Y_train, c)
        W = np.array(solution['x'][0:57])
        bias = solution['x'][3056]
        print('BIAS :', bias)
        
        N_train, D_train = X_train.shape
        error_train = score(W, X_train, Y_train, bias)
        print('ERROR ON TRAINING DATA : ', (1 - error_train/N_train)*100)
        
        N_val, D_val = X_val.shape
        error_val = score(W, X_val, Y_val, bias)
        print('ERROR ON VALIDATION DATA : ', (1 - error_val/N_val)*100)
        
        N_test, D_test = X_test.shape
        error_test = score(W, X_test, Y_test, bias)
        print('ERROR ON VALIDATION DATA : ', (1 - error_test/N_train)*100)
        
        if error_val <= min_error_val and error_train <= min_error_train:
            best_c = c
            best_solution = solution
            min_error_val = error_val
            min_error_train = error_train
        
        print('---------------------------------------------------------------------------------------')
    
    
   
    W = np.array(best_solution['x'][0:57])
    bias = best_solution['x'][3056]
    error_test = score(W, X_test, Y_test, bias)
    
    print('BEST C OBTAINED ', best_c)
    print('TEST ERROR ON DATA SET : ', error_test)    
        
    return (best_solution, best_c)

best_solution, best_c = fit_best_svm()
    
    
    
    
    
    
    
    
    
    
    
