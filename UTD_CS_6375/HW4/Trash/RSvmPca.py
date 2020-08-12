# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 14:06:16 2020

@author: ROHITH PEDDI
"""

import pandas as pd
import numpy as np
import cvxopt as cpt


#Reading the data using pandas
Train_data = pd.read_csv('sonar_train.data',header = None)
Test_data = pd.read_csv('sonar_test.data',header = None)
Validation_data = pd.read_csv('sonar_valid.data',header = None)

#setting 0 to -1 in the target
m = len(Train_data.columns)-1
Train_data.loc[Train_data[m] == 2, m] = -1
m = len(Test_data.columns)-1
Test_data.loc[Test_data[m] == 2, m] = -1
m = len(Validation_data.columns)-1
Validation_data.loc[Validation_data[m] == 2, m] = -1

def splitData(data): #Splits Train data separating labels
    m = len(data.columns)-1
    x = np.array(data.iloc[:,0:m])
    y = np.array(data.iloc[:,m])
    return x, y    

def computeCovarianceMatrix(data):
    mat = data
    m = len(data)
    mean = (data.sum(axis=0))/m
    n = len(data)
    for i in range(n):
        mat[i] = mat[i] - mean
    mat = mat.transpose()
    mat = np.matmul(mat, mat.transpose())
    return mat
 
    
def eigen(matrix): #Method for calculating Eigen Values and Eigen Vectors
    eigenValues, eigenVectors = np.linalg.eig(matrix) 
    idx = eigenValues.argsort()[::-1][0:6]     #[0:6] selects the top 6 eigen values
    eigenValues = eigenValues[idx]  
    eigenVectors = eigenVectors[:, idx]
    return eigenValues, eigenVectors
    

#Accuracy Computation
def computeAccuracy(x, y, w, b):#Given data, w and b computeAccuracy calculates accuracy
    x = np.asarray(x)
    count = 0
    length = len(x)
    for i in range(length):
        f = np.dot(w, x[i]) + b
        if f * y[i] > 0:
            count += 1
    accuracy = count/length * 100
    return accuracy


#Methods for calculating P, H, Q AND G 
def computeP(m, n):
    P = np.zeros((m+n+1, m+n+1))
    for i in range(n):
        P[i][i] = 1
    return cpt.matrix(P)
    
def computeH(m):
    H = np.zeros((2*m, 1))
    for i in range(m):
        H[i][0] = -1
    return cpt.matrix(H)

def computeQ(m, n, c):
    Q = np.zeros((m+n+1, 1))
    for i in range(n, m+n):
        Q[i][0] = c
    return cpt.matrix(Q)

def computeG(Train_x, Train_y, m, n):
    a = np.zeros((m, n))
    b = np.zeros((m, n))
    for i in range(m):
        for j in range(n):
            a[i][j] = - Train_y[i] * Train_x[i][j]
    x = np.vstack((a, b)) #hstack
            
    c = np.identity(m) * -1
    d = np.identity(m) * -1
    y = np.vstack((c, d))
            
    e = np.ones((m, 1)) * -1
    for i in range(m):
        e[i] = e[i] * Train_y[i]
    f = np.zeros((m,1))
    z = np.vstack((e, f))
    GMat = np.hstack((x, y, z))
    G = cpt.matrix(GMat)
    return G

def ProjectData(data): #Projecting the data using PCA
    data_x, data_y = splitData(data)
    CovarianceMatrix = computeCovarianceMatrix(data_x)
    eigenValues, eigenVectors = eigen(CovarianceMatrix) 
    m = len(data.columns)-1
    data = np.array(data.iloc[:,0:m])
    data_x = np.matmul(data, eigenVectors) #Projecting the data into new dimensional place
    return data_x, data_y, eigenVectors


def ProjectData1(data, eigenVectors):
    data, data_y = splitData(data)
    data_x = np.matmul(data, eigenVectors) #Projecting the data into new dimensional place
    return data_x, data_y
    
    
    
#Projects the training, testing and validation data into 6 dimensions w.r.to frobenious form
data_x, data_y, eigenVectors = ProjectData(Train_data)
valid_x, valid_y = ProjectData1(Validation_data, eigenVectors)
test_x, test_y = ProjectData1(Test_data, eigenVectors)


k = 6 #K values
C =[1, 10, 100, 1000]   #C values
m = len(data_x)  #number of rows
finalWeight = []
finalBias = 0
bestAccuracy = 0
bestK = 0
bestC = 0
for i in range(k):
    data_k = data_x[:, 0:i+1]
    valid_k = valid_x[:, 0:i+1]
    n = data_k.shape[1]   #number of columns
    P = computeP(m, n)
    G = computeG(data_k, data_y, m, n)
    h = computeH(m)
    for j in C:
        q = computeQ(m, n, j)
        #Quadratic Programming cvxopt solver
        result = cpt.solvers.qp(P, q, G, h)
        lst = result['x']
        #Weight Calculation
        weight = []
        for k in range(n):
            weight.append(lst[k]) 
        #bias
        bias = lst[m+n]
        acc = computeAccuracy(data_k, data_y, weight, bias)
        acc = computeAccuracy(valid_k, valid_y, weight, bias)
        print('Error on Validation data set is',100-acc,' for value of C =',j,'and K =',i+1)
        if(acc > bestAccuracy): #Tuning the value of c and K from Validation set
            finalWeight = weight
            finalBias = bias
            bestAccuracy = acc
            bestK = i+1
            bestC = j
            
        
print('The best pair of k and c value is',bestK,'and',bestC)
#Accuracy on testing set
accuracy_proj = computeAccuracy(test_x[:, 0:bestK], test_y, finalWeight, finalBias)
print('Error on testing set of Projected Data is', 100-accuracy_proj)





"""
Calculating the estimator of error on the original data instead of Projection
"""
data_x, data_y = splitData(Train_data)
valid_x, valid_y = splitData(Validation_data)
test_x, test_y = splitData(Test_data)
C =[1, 10, 100, 1000]   #C values
m = len(data_x)  #number of rows
finalWeight = []
finalBias = 0
bestAccuracy = 0
bestC = 0
n = data_x.shape[1]  #number of columns
print(n)
P = computeP(m, n)
G = computeG(data_x, data_y, m, n)
h = computeH(m)
for j in C:
    #print(j)
    print('----------------------------------------------------------------')
    print('Calculating for c ', j)
    q = computeQ(m, n, j)
    #Quadratic Programming cvxopt solver
    result = cpt.solvers.qp(P, q, G, h)
    lst = result['x']
    #Weight Calculation
    weight = []
    for k in range(n):
        weight.append(lst[k]) 
    #bias
    bias = lst[m+n]
    print('BIAS ', bias)
    #print(data_x.shape)
   
    acc = computeAccuracy(data_x, data_y, weight, bias)
    print('ACCURACY ON TRAINING DATA : ', acc)
    acc = computeAccuracy(valid_x, valid_y, weight, bias)
    print('ACCURACY ON VALIDATION DATA : ', acc)
    acc = computeAccuracy(test_x, test_y, weight, bias)
    print('ACCURACY ON TEST DATA : ', acc)
    if(acc > bestAccuracy): #Tuning the value of c and K from Validation set
        finalWeight = weight
        finalBias = bias
        bestAccuracy = acc
        bestC = j
            
        
print('The best c value on original data is',bestC)
#Accuracy on testing set
print('Error on testing set on the original data is', 100-computeAccuracy(test_x, test_y, finalWeight, finalBias))

print('Error on testing set of Projected Data is', 100-accuracy_proj)











