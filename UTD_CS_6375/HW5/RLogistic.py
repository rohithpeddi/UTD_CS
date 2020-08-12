# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 09:34:35 2020

@author: ROHITH PEDDI
"""

import numpy as np
import pandas as pd

Train_data = pd.read_csv('sonar_train.data', header = None).values
Test_data = pd.read_csv('sonar_valid.data', header = None).values
Validation_data = pd.read_csv('sonar_test.data', header = None).values

M, N = Train_data.shape
#setting 0 to -1 in the target

Train_data[Train_data[:, N-1] == 2, N-1] = -1
Test_data[Test_data[:, N-1] == 2, N-1] = -1
Validation_data[Validation_data[:, N-1] == 2, N-1] = -1

def sigmoid_function(theta):
    s = 1 / (1 + np.exp(-theta))
    return s

def compute_loss(data, weight, bias):
    m = data.shape[0]
    loss = 0
    for i in range(m):
        x = data[i, 1:]
        y = data[i, 0]
        k = np.dot(weight.T, x) + bias
        #print(1 + np.exp(k))
        loss += y*k - np.log(1 + np.exp(k))
    return loss

def logistic_regression(data, weight, bias, step):
    m = data.shape[0]
    loss = compute_loss(data, weight, bias)
    it = 0
    while True:
        it += 1
        gradient_w = 0
        gradient_b = 0
        for i in range(m):
            x = data[i, 1:]
            k = np.dot(weight.T, x) + bias
            p = sigmoid_function(k)
            gradient_w += x * ((data[i, 0]+1)/2 - p)
            gradient_b += ((data[i, 0]+1)/2 - p)
        w = weight + step * gradient_w
        b = bias + step * gradient_b
        loss1 = compute_loss(data, weight, bias)
        if loss1 - loss < 0.0001 and it >= 2:
            break
        loss = loss1
        weight = w
        bias = b
    print("Iterations", it)
    return w, b

def logistic_regression_l1(data, weight, bias, step, l1):
    m, n = data.shape
    n -= 1
    wt = np.array([1] * n)
    loss = compute_loss(data, weight, bias)
    it = 0
    while True:
        it += 1
        gradient_w = 0
        gradient_b = 0
        for i in range(m):
            x = data[i, 1:]
            k = np.dot(weight.T, x) + bias
            p = sigmoid_function(k)
            gradient_w += x * ((data[i, 0]+1)/2 - p)
            gradient_b += ((data[i, 0]+1)/2 - p)
        gradient_w = gradient_w - l1 * wt
        w = weight + step * gradient_w
        b = bias + step * gradient_b
        loss1 = compute_loss(data, weight, bias) - l1 * np.linalg.norm(weight)
        if loss1 - loss < 0.0001 and it >= 2:
            break
        loss = loss1
        weight = w
        bias = b
    return w, b             
            
def logistic_regression_l2(data, weight, bias, step, l2):
    m = data.shape[0]
    it = 0
    loss = compute_loss(data, weight, bias)
    while True:
        it += 1
        gradient_w = 0
        gradient_b = 0
        for i in range(m):
            x = data[i, 1:]
            k = np.dot(weight.T, x) + bias
            p = sigmoid_function(k)
            gradient_w += x * ((data[i, 0]+1)/2 - p)
            gradient_b += ((data[i, 0]+1)/2 - p)
        gradient_w = gradient_w - (l2 * weight)
        w = weight + step * gradient_w
        b = bias + step * gradient_b
        loss1 = compute_loss(data, weight, bias) - l2 * (np.linalg.norm(weight) ** 2)
        if loss1 - loss < 0.0001 and it >= 2:
            break
        loss = loss1
        weight = w
        bias = b
    return w, b           
            


def accuracy(data, weight, bias):
    m = data.shape[0]
    cnt = 0
    for i in range(m):
        x = data[i, 1:]
        t = np.dot(weight.T, x) + bias
        if t > 0:
            if data[i, 0] > 0:
                cnt += 1
        else:
            if data[i, 0] < 0:
                cnt += 1
    return cnt/m * 100



cols = Train_data.shape[1] - 1
weight = [0.25] * cols
weight = np.array(weight)
bias = 0.75
learningRate = [0.000001] #Defines the step size learning rate


acc = 0
for lr in learningRate:
    w, b = logistic_regression(Train_data, weight, bias, lr)
    valid_acc = accuracy(Validation_data, w, b)
    print("Validation accuracy is",valid_acc)
    if valid_acc >= acc:
        acc = valid_acc
        finalWeight = w
        finalBias = b

print(finalWeight)  
print('Accuarcy on test data is', accuracy(Test_data, finalWeight, finalBias))

print('----------------------------------------------------------------------------')

acc = 0
l2 = [0.0001, 0.001, 0.01, 0.1, 0.5, 1, 10, 100, 1000]
for lr in learningRate:
    for i in l2:
        w, b = logistic_regression_l2(Train_data, weight, bias, lr, i)
        valid_acc = accuracy(Validation_data, w, b)
        print("Validation accuracy for l2=",i,"is",valid_acc)
        if valid_acc >= acc:
            bestl2 = i
            acc = valid_acc
            finalWeight = w
            finalBias = b

print("Weight vector of l2 regularization", finalWeight)  
print("Bias of l2 regularization", finalBias)
print("Best l2 constant",bestl2)
print('Accuarcy on test data with l2 penalty is', accuracy(Test_data, finalWeight, finalBias))
        
print('----------------------------------------------------------------------------')
    
#Logistic Regression 
acc = 0
l1 = [0.0001, 0.001, 0.01, 0.1, 0.5, 1, 10, 100, 1000]
for lr in learningRate:
    for i in l1:
        w, b = logistic_regression_l1(Train_data, weight, bias, lr, i)
        valid_acc = accuracy(Validation_data, w, b)
        print("Validation accuracy for l1=",i,"is",valid_acc)
        if valid_acc >= acc:
            bestl1 = i
            acc = valid_acc
            finalWeight = w
            finalBias = b

print("Weight vector of l1 regularization", finalWeight)  
print("Bias of l1 regularization", finalBias)
print("Best l1 constant",bestl1)
print('Accuarcy on test data with l1 penalty is', accuracy(Test_data, finalWeight, finalBias))                

print('----------------------------------------------------------------------------')