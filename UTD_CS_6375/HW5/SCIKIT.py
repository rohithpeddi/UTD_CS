# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 08:50:55 2020

@author: ROHITH PEDDI
"""

import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB

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

def accuracy(Y_pred, Y):
    M,N = Y_pred.shape
    misclassifications =  np.sum(abs(Y-Y_pred))/2
    return (1- misclassifications/M)*100

def linear_svm_check(X_train, Y_train, X_test, Y_test):
    clf = SVC(gamma='auto', kernel='linear')
    #clf = SVC(gamma='auto')
    clf.fit(X_train, Y_train)
    train_accuracy = accuracy(clf.predict(X_train).reshape(-1, 1), Y_train)
    test_accuracy = accuracy(clf.predict(X_test).reshape(-1,1), Y_test)
    print('TRAIN ACCURACY ' , train_accuracy, ', TEST ACCURACY ', test_accuracy)
    
def logistic_check(X_train, Y_train, X_val, Y_val, X_test, Y_test):   
    clf = LogisticRegression(penalty='none', tol=1e-7, max_iter=10000000, solver='saga').fit(X_train, Y_train)
    train_accuracy = clf.score(X_train, Y_train)
    validation_accuracy = clf.score(X_val, Y_val)
    test_accuracy = clf.score(X_test, Y_test)
    print('-----------------------------------------------------------')
    print('TRAINING ACCURACY ', train_accuracy)
    print('VALIDATION ACCURACY ', validation_accuracy)            
    print('TEST ACCURACY ', test_accuracy)
    print('-----------------------------------------------------------')

def logistic_check_l1(X_train, Y_train, X_val, Y_val, X_test, Y_test):
    L1 = np.empty((14, 4))
    #C = [0.000001, 0.00001, 0.0001, 0.001, 0.01, 0.1, 0.5, 1, 10, 100, 1000, 10000, 100000, 1000000]
    C = [100000]
    index = 0
    for c in C:
        L1[index, 0] = c
        clf = LogisticRegression(C=c, penalty='l1', tol=1e-7, max_iter=10000000, solver='saga').fit(X_train, Y_train)
        train_accuracy = clf.score(X_train, Y_train)
        validation_accuracy = clf.score(X_val, Y_val)
        test_accuracy = clf.score(X_test, Y_test)
        print('-----------------------------------------------------------')
        print('L1 FOR C: ', c)
        print('TRAINING ACCURACY ', train_accuracy)
        print('VALIDATION ACCURACY ', validation_accuracy)            
        print('TEST ACCURACY ', test_accuracy)
        print('-----------------------------------------------------------')
        L1[index, 1] = train_accuracy
        L1[index, 2] = validation_accuracy
        L1[index, 3] = test_accuracy
        index = index + 1
    
    return L1
        
    
def logistic_check_l2(X_train, Y_train, X_val, Y_val, X_test, Y_test):
    L2 = np.empty((14, 4))
    #C = [0.000001, 0.00001, 0.0001, 0.001, 0.01, 0.1, 0.5, 1, 10, 100, 1000, 10000, 100000, 1000000]
    C = [100000]
    index = 0
    for c in C:
        L2[index, 0] = c
        clf = LogisticRegression(C=c, penalty='l2', tol=1e-7, max_iter=10000000, solver='saga').fit(X_train, Y_train)
        train_accuracy = clf.score(X_train, Y_train)
        validation_accuracy = clf.score(X_val, Y_val)
        test_accuracy = clf.score(X_test, Y_test)
        print('-----------------------------------------------------------')
        print('L2 FOR C: ', c)
        print('TRAINING ACCURACY ', train_accuracy)
        print('VALIDATION ACCURACY ', validation_accuracy)            
        print('TEST ACCURACY ', test_accuracy)
        print('-----------------------------------------------------------')
        L2[index, 1] = train_accuracy
        L2[index, 2] = validation_accuracy
        L2[index, 3] = test_accuracy
        index = index + 1
    
    return L2
        
def naive_bayes_check(X_train, Y_train, X_test, Y_test):
    clf = GaussianNB()
    clf.fit(X_train, Y_train)
    training_accuracy = clf.score(X_train, Y_train)
    test_accuracy = clf.score(X_test, Y_test)
    print('-----------------------------------------------------------')
    print('TRAINING ACCURACY ', training_accuracy)
    print('TEST ACCURACY ', test_accuracy)
    print('-----------------------------------------------------------')
    return clf

(X_train, Y_train) = prepare_data(data_train)
(X_val, Y_val) = prepare_data(data_val)
(X_test, Y_test) = prepare_data(data_test)
#linear_svm_check(X_train, Y_train, X_test, Y_test)

print('###################################################################')
print('###################################################################')
print('###################################################################')
print('###################################################################')
#logistic_check(X_train, Y_train, X_val, Y_val, X_test, Y_test)
print('###################################################################')
print('###################################################################')
print('###########################   L1    ###############################')
print('###################################################################')
print('###################################################################')
L1 = logistic_check_l1(X_train, Y_train, X_val, Y_val, X_test, Y_test)
print('###################################################################')
print('###################################################################')
print('########################      L2     ##############################')
print('###################################################################')
print('###################################################################')
L2 = logistic_check_l2(X_train, Y_train, X_val, Y_val, X_test, Y_test)
print('###################################################################')

#clf = naive_bayes_check(X_train, Y_train, X_test, Y_test)