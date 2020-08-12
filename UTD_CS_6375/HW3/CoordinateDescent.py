# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 21:44:39 2020

@author: ROHITH PEDDI
"""
import pandas as pd
import numpy as np

data_train = pd.read_csv('heart_train.data')
data_test = pd.read_csv('heart_test.data')

data_train.columns = ['Y', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12', 'F13', 'F14', 'F15', 'F16', 'F17', 'F18', 'F19', 'F20', 'F21', 'F22']
data_test.columns = ['Y', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12', 'F13', 'F14', 'F15', 'F16', 'F17', 'F18', 'F19', 'F20', 'F21', 'F22']

data_train['Y'][data_train['Y'] == 0] = -1
data_test['Y'][data_test['Y'] == 0] = -1

##########################################################################################################
################################# DECISION STUMP IMPLEMENTATION ###########################################
##########################################################################################################

class Node(object):    
    
    def __init__(self, data, parent_attr_value):
        self.data = data
        self.children = []
        self.attr = None
        self.decision = None
        self.parent_attr = None
        self.parent_attr_value = parent_attr_value

class DT(object):
    
    def __init__(self, data, attr, is_0p, is_all_pos):
        self.data = data
        self.attr = attr
        self.is_0p = is_0p
        self.is_all_pos = is_all_pos
        self.root = None
        self.training_error = None
        
    def classify(self):
        node = Node(self.data, None)
        self.root = node 
        self.build_tree(node)
        
    def build_tree(self, node):        
        data = node.data
        attr = self.attr
        is_0p = self.is_0p
        is_all_pos = self.is_all_pos
        
        if is_all_pos is not None:
            node.decision = 1 if is_all_pos else -1
            node.attr = 'POSITIVE' if is_all_pos else 'NEGATIVE'
            return
        
        attr_values = data[attr].unique()    
        node.attr = attr
        
        for attr_value in attr_values:
            split = data[data[attr] == attr_value]
            child = Node(split, attr_value)
            child.parent_attr = attr
            node.children.append(child)
            
            if attr_value == 0 and is_0p: 
                child.decision = 1
            elif attr_value == 1 and is_0p:
                child.decision = -1
            elif attr_value == 0 and not is_0p:
                child.decision = -1
            elif attr_value == 1 and not is_0p:
                child.decision = 1
                
    
    def predict_dataset(self, data):    
        Y_pred = []
        for i in range(0, len(data)):
            prediction = self.predict(self.root, data.iloc[i])
            Y_pred.append(prediction)
        return Y_pred
    
    def predict(self, node, data_point):        
        if node.decision is not None:
            return node.decision    
        attr = node.attr            
        child = None
        for child in node.children:        
            if child.parent_attr_value == data_point[attr]:
                break              
        return self.predict(child, data_point)       
         
##########################################################################################################
################################# COORDINATE DESCENT IMPLEMENTATION ######################################
##########################################################################################################

def build_hypotheses(data):
    classifiers = []
    
    all_positive = DT(data, None, None, True)
    all_negative = DT(data, None, None, False)
    
    classifiers.append(all_negative)
    classifiers.append(all_positive)
    
    for attr in data.columns:
        if attr == 'Y' or attr == 'W':
            continue
        
        classifier = DT(data, attr, True, None)
        classifiers.append(classifier)
        
        classifier = DT(data, attr, False, None)
        classifiers.append(classifier)
        
    for i in range(len(classifiers)):
        classifiers[i].classify()
        
    return classifiers

def fetchMinAlpha(alphas, classifiers, data, position):
    current_alpha = alphas[position]    
    M,N = data.shape
    
    Y = data['Y'].values.reshape(M, 1)
    Y_pred = np.array(classifiers[position].predict_dataset(data)).reshape(M, 1)
    misclassifications = abs(Y-Y_pred)
    
    misclassifications_indices = np.where(misclassifications > 0)[0]
    correct_classification_indices = np.where(misclassifications <= 0)[0]
    
    misclassified_data = data.iloc[misclassifications_indices]
    correctly_classified_data = data.iloc[correct_classification_indices]
    
    misclassified_data_length = len(misclassifications_indices)
    correctly_classified_data_length = len(correct_classification_indices)
    
    Y_misclassified = data['Y'].iloc[misclassifications_indices].values.reshape((misclassified_data_length,1))
    Y_correctly_classified = data['Y'].iloc[correct_classification_indices].values.reshape((correctly_classified_data_length,1))  
    
    Y_pred_misclassified = np.zeros((misclassified_data_length,1))
    Y_pred_correctly_classified = np.zeros((correctly_classified_data_length, 1))
    
    for i in range(len(alphas)):        
        if i == position:
            continue
        
        alpha = alphas[i]
        Y_pred_misclassified = Y_pred_misclassified + alpha*(np.array(classifiers[i].predict_dataset(misclassified_data)).reshape(misclassified_data_length,1))
        Y_pred_correctly_classified = Y_pred_correctly_classified + alpha*(np.array(classifiers[i].predict_dataset(correctly_classified_data)).reshape(correctly_classified_data_length,1))
        
    correctly_classified = np.exp(-1.0 * Y_correctly_classified * Y_pred_correctly_classified).sum()
    misclassified = np.exp(-1.0 * Y_misclassified * Y_pred_misclassified).sum()
    
    modified_alpha = 0.5 * np.log(correctly_classified/misclassified)
    
    return (alphas, modified_alpha, modified_alpha-current_alpha)
    

def fetchNextMinAdjustedAlphas(alphas, classifiers, data, counter):
    N_c = len(alphas)    
    current = counter + 1
    isRoundRobinComplete = False    
    while not isRoundRobinComplete :
        (alphas, modified_alpha, difference) = fetchMinAlpha(alphas, classifiers, data, (current%N_c))
        print('C ALPHA ', alphas[current%N_c], 'M ALPHA', modified_alpha, 'DIFFERENCE ', difference, ', POSITION ', current)
        if abs(difference) > 1e-4:
            alphas[current%N_c] = modified_alpha
            return (alphas, current%N_c)
        
        if current-counter > N_c:
            isRoundRobinComplete = True
            return (alphas, None)
        
        current = current+1   

def coordinate_descent(data, classifiers):    
    N_c = len(classifiers)
    alphas = np.zeros(N_c).reshape(N_c,1)
    
    iterations = counter = 0
    is_local_optimum = False
    while not is_local_optimum:
        (alphas, counter) = fetchNextMinAdjustedAlphas(alphas, classifiers, data, counter)
        
        iterations = iterations+1
        if counter is None:
            is_local_optimum = True
            break
        
        print('--------------------------------------------------------')
        print('ITERATION ', iterations, ', ATTRIBUTE ', counter)
        print('--------------------------------------------------------')
    
    print('ALPHAS ', alphas)
    
    return alphas

def accuracy(data, alphas, classifiers):
    M, N = data.shape
    Y = data['Y'].values.reshape(M,1)
    Y_pred = np.zeros(M).reshape(M,1)
    
    N_c = len(classifiers)
    
    for i in range(N_c):
        alpha = alphas[i]
        Y_pred = Y_pred + alpha*(np.array(classifiers[i].predict_dataset(data)).reshape(M,1))
        
    
    Y_pred[Y_pred < 0] = -1
    Y_pred[Y_pred >= 0] = 1
    #print(Y-Y_pred)
    
    misclassification = sum(abs(Y-Y_pred))/2
    
    return (1.0 - misclassification/M ) * 100

classifiers = build_hypotheses(data_train)
alphas = coordinate_descent(data_train, classifiers)
training_accuracy = accuracy(data_train, alphas, classifiers)
print('ACCURACY ON TRAINING DATA : ', training_accuracy)
test_accuracy = accuracy(data_test, alphas, classifiers)
print('ACCURACY ON TEST DATA : ', test_accuracy)

        
        
        
    
    
    
    
    