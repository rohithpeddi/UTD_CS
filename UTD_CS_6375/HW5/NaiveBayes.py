# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 19:37:08 2020

@author: ROHITH PEDDI
"""

import math
import pandas as pd
import numpy as np

data_train = pd.read_csv('sonar_train.data', header = None)
data_test = pd.read_csv('sonar_test.data', header = None)

data_test.columns = data_train.columns = ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10',
        'F11', 'F12', 'F13', 'F14', 'F15', 'F16', 'F17', 'F18', 'F19',
        'F20', 'F21', 'F22', 'F23', 'F24', 'F25', 'F26', 'F27', 'F28',
        'F29', 'F30', 'F31', 'F32', 'F33', 'F34', 'F35', 'F36', 'F37',
        'F38', 'F39', 'F40', 'F41', 'F42', 'F43', 'F44', 'F45', 'F46',
        'F47', 'F48', 'F49', 'F50', 'F51', 'F52', 'F53', 'F54', 'F55',
        'F56', 'F57', 'F58', 'F59', 'F60', 'F61']

def class_priors(Y, classes):
    M, N = Y.shape
    class_probabilities = []
    for cl in classes:
        split = Y[Y == cl]
        M_y, N_y = split.shape
        class_probabilities.append(M_y/M)
    return class_probabilities

def get_params(data, classes):
    M, N = data.shape
    means = []
    variances = []
    for cl in classes:
        split = data[data['F61'] == cl].iloc[:, 0:60]
        mean = np.array(np.mean(split, axis=0)).reshape(1, N-1)
        variance = np.array(np.var(split, axis=0)).reshape(1, N-1)
        means.append(mean)
        variances.append(variance)        
    return (means, variances)   

def get_probability(mean, variance, data_point):
    exponents = ((data_point-mean)**2)/(2*variance)
    exponents = np.exp(-exponents)
    constants = 1/( np.sqrt( 2*np.pi*variance ) )
    probabilities = constants*exponents
    return np.prod(probabilities)

def accuracy(data, P_y_1, P_y_2, m_1, m_2, variance_1, variance_2):
    M, N = data.shape    
    Y = data['F61']
    data = data.iloc[:, 0:60]
    misclassifications = 0
    Y_pred = []
    for i in range(M):
        data_point = np.array(data.loc[i]).reshape(1, 60)
        P_1 = get_probability(m_1, variance_1, data_point)
        P_2 = get_probability(m_2, variance_2, data_point)        
        
        if P_1 > P_2 :
            if Y[i] == 2:
                misclassifications = misclassifications + 1
                Y_pred.append(1)
        else :
            if Y[i] == 1:
                misclassifications = misclassifications + 1
                Y_pred.append(2)
        
    return (1 - misclassifications/M)*100

classes = [1, 2]
class_prior_probabilities = class_priors(data_train, classes)
P_y_1 = class_prior_probabilities[0]
P_y_2 = class_prior_probabilities[1]

(means, variances) = get_params(data_train, classes)
m_1 = means[0]
m_2 = means[1]
variance_1 = variances[0]
variance_2 = variances[1]

test_accuracy = accuracy(data_test, P_y_1, P_y_2, m_1, m_2, variance_1, variance_2)
print('ACCURACY ON TEST DATA ', test_accuracy)
