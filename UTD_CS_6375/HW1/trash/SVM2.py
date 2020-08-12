#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 22:11:06 2020

@author: rohith
"""

import pandas as pd

import numpy as np
import quadprog as quad

 ##Quadratic programming Reference as posted in piazza but using quadprog 
 #package instead of CVXOPT
 ## https://courses.csail.mit.edu/6.867/wiki/images/a/a7/Qp-cvxopt.pdf
    
data = pd.read_csv('mystery.data',header = None)
rows = len(data)
G = np.zeros((rows,16))


def Solve(P, q, G=None, h=None):  #Quad Prog Solving
    return quad.solve_qp(.5 * P, q, -G.T,  -h, 0)[0]


 # Feature vector [x0**3, x1**3,x2**3,x3**3,x0 ** 2,x1 ** 2,x2 ** 2,x3 ** 2,x0 * x1,x1 * x2,x2 * x3,x0,x1,x2,x3]
def features(train_data, rows):
    featuredData = np.empty((1000,16), dtype=float)
    for k in range(rows):
        x0 = data.iloc[k, 0];
        x1 = data.iloc[k, 1];
        x2 = data.iloc[k, 2];
        x3 = data.iloc[k, 3];
        y = data.iloc[k, 4]
        featuredData[k, 0] = x0 ** 3
        featuredData[k, 1] = x1 ** 3
        featuredData[k, 2] = x2 ** 3
        featuredData[k, 3] = x3 ** 3
        featuredData[k, 4] = x0 ** 2
        featuredData[k, 5] = x1 ** 2
        featuredData[k, 6] = x2 ** 2
        featuredData[k, 7] = x3 ** 2
        featuredData[k, 8] = x0 * x1
        featuredData[k, 9] = x1 * x2
        featuredData[k, 10] = x2 * x3
        featuredData[k, 11] = x0
        featuredData[k, 12] = x1
        featuredData[k, 13] = x2
        featuredData[k, 14] = x3
        featuredData[k, 15] = y
        G[k, 0] = -featuredData[k, 0] * y
        G[k, 1] = -featuredData[k, 1] * y
        G[k, 2] = -featuredData[k, 2] * y
        G[k, 3] = -featuredData[k, 3] * y
        G[k, 4] = -featuredData[k, 4] * y
        G[k, 5] = -featuredData[k, 5] * y
        G[k, 6] = -featuredData[k, 6] * y
        G[k, 7] = -featuredData[k, 7] * y
        G[k, 8] = -featuredData[k, 8] * y
        G[k, 9] = -featuredData[k, 9] * y
        G[k, 10] = -featuredData[k, 10] * y
        G[k, 11] = -featuredData[k, 11] * y
        G[k, 12] = -featuredData[k, 12] * y
        G[k, 13] = -featuredData[k, 13] * y
        G[k, 14] = -featuredData[k, 14] * y
        G[k, 15] = -y

    return featuredData, G

data, G = features(data, rows)
#print(data[0,1])

P = np.zeros((16,16))
for i in range(16):
    P[i, i] = 1;
q = np.zeros((16,1)).reshape((16,))
h = -np.ones((1,1000))
h = -np.ones((rows,1)).reshape((len(data),))
#print(P)


   


W = Solve(P,q,G,h)   #Quadratic prog solve

print("Weight ", W[:15])  #Weight
print("bias ", W[15])   #bias

print("Margin ",  (1 / np.sqrt((W[0:15] ** 2).sum())))   #Margin = 1/||W||


i = 0

#Test
supportVectors = []
predicted = []
while(i < 1000):
    j = 0
    k = 0
    while(j < 15):
        k = k + W[j]*data[i, j]
        j = j+ 1
    k = k+W[15]
    if(k > 0 and k <= 1.00000000000002):
        supportVectors.append(data[i])
        predicted.append(k)
    elif(int(k) == -1):
        predicted.append(k)
        supportVectors.append(data[i])
    #print("predicted ",k," actual ", data[i, j])
    i = i+1
    
#print(supportVectors)
#print(predicted)
supportVectorLength = len(supportVectors)
i = 0
print("\nThe Support Vectors are ")
while(i < supportVectorLength):
    print(supportVectors[i],"\n")
    i += 1

