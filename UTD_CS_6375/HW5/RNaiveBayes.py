# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 09:37:51 2020

@author: ROHITH PEDDI
"""

import pandas as pd
import numpy as np
import math

#Reading the data using pandas
Train_data = pd.read_csv('sonar_train.data',header = None)
Test_data = pd.read_csv('sonar_test.data',header = None)

def calculateProbability(x, mean, stdev):
    exponent = math.exp(-(math.pow(x-mean,2)/(2*math.pow(stdev,2))))
    return (1 / (math.sqrt(2*math.pi) * stdev)) * exponent

m = len(Train_data.columns)-1
data = {}
data[1] = np.array(Train_data.loc[Train_data[m] == 1])
data[2] = np.array(Train_data.loc[Train_data[m] == 2])

data_summary = {}
for key, value in data.items():
    data_k = value
    data_summary[key] = {}
    for i in range(m):
        tree = {}
        tree['mean'] = np.mean(data_k[:, i])
        tree['sd'] = np.std(data_k[:, i])
        data_summary[key][i] = tree
        
Test_data = np.array(Test_data)
#Accuracy on Test Data
n = len(Test_data)
count = 0
for i in range(n):
    r = Test_data[i,:]
    p1 = 1
    p2 = 1
    for j in range(m):
        mean = data_summary[1][j]['mean']
        std = data_summary[1][j]['sd']
        p1 = p1 * calculateProbability(r[j], mean, std)
        mean = data_summary[2][j]['mean']
        std = data_summary[2][j]['sd']
        p2 = p2 * calculateProbability(r[j], mean, std)
    if p1 > p2:
        if r[m] == 1:
            count += 1
    else:
        if r[m] == 2:
            count += 1
        
        
test_accuracy = count/n * 100
print('Accuracy on test data is', test_accuracy)        
    
    

