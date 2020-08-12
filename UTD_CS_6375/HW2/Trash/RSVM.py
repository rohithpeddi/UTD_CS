#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 09:42:03 2020

@author: rohith
"""

import pandas as pd
import numpy as np
import cvxopt as cpt

Train_data = pd.read_csv('spam_train.data',header = None)
Test_data = pd.read_csv('spam_test.data',header = None)
Validation_data = pd.read_csv('spam_validation.data',header = None)

#setting 0 to -1 in the target
Train_data.loc[Train_data[57] == 0, 57] = -1
Test_data.loc[Test_data[57] == 0, 57] = -1
Validation_data.loc[Validation_data[57] == 0, 57] = -1

m = len(Train_data)  #number of rows
n = len(Train_data.columns)-1   #number of columns


def split_data(data):
    x = np.array(data.iloc[:,0:57])
    y = np.array(data.iloc[:,57])
    return (x, y)

#Training
Train_x, Train_y = split_data(Train_data)
#validation
valid_x, valid_y = split_data(Validation_data)
#Testing
Test_x, Test_y = split_data(Test_data)

def computeAccuracy(data, w, b):#Given data, w and b computeAccuracy calculates accuracy
    x, y = split_data(data)
    length = len(data)
    count = 0
    for i in range(length):
        f = np.dot(w, x[i]) + b
        if f * y[i] > 0:
            count += 1
    accuracy = count/length * 100
    return accuracy
    

def computeP():
    P = np.zeros((m+n+1, m+n+1))
    for i in range(n):
        P[i][i] = 1
    return cpt.matrix(P)
    

def computeH():
    H = np.zeros((2*m, 1))
    for i in range(m):
        H[i][0] = -1
    return cpt.matrix(H)

def computeQ(c):
    Q = np.zeros((m+n+1, 1))
    for i in range(n, m+n):
        Q[i][0] = c
    return cpt.matrix(Q)
    
def computeG():
    G = np.zeros((2*m, m+n+1))
    for i in range(m):
        for j in range(n):
            G[i][j] = -1 * Train_y[i] * Train_x[i][j]
        G[i][n+i] = -1
        G[i][m+n] = -1 * Train_y[i]
        G[m+i][n+i] = -1
    return cpt.matrix(G)

P = computeP()
G = computeG()
h = computeH()

finalWeight = []
finalBias = 0
bestAccuracy = 0
bestC = []
for i in range(0, 9):
    c = 10 ** i
    q = computeQ(c)
    #Quadratic Programming cvxopt solver
    result = cpt.solvers.qp(P, q, G, h)
    lst = result['x']
    #Weight Calculation
    weight = []
    for j in range(n):
        weight.append(lst[j]) 
    #bias
    bias = lst[m+n]
    acc = computeAccuracy(Train_data, weight, bias)
    print('Accuracy on Training data set is',acc,' for value of C =',c)
    acc = computeAccuracy(Validation_data, weight, bias)
    print('Accuracy on Validation data set is',acc,' for value of C =',c)
    if(acc >= bestAccuracy):
        if acc > bestAccuracy:
            bestC = []
        finalWeight = weight
        finalBias = bias
        bestC.append(c)
        bestAccuracy = acc
    
    
#Tuning the value of c from Validation set
print('The best values of c that are tuned from Validation set are',bestC)

#Accuracy on testing set
print('Accuracy on testing set is', computeAccuracy(Test_data, finalWeight, finalBias))

    
    
    
    
    
    
    
    
    
    
    
    
    
    
