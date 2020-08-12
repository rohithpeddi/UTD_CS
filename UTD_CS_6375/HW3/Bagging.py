# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 21:21:50 2020

@author: ROHITH PEDDI
"""

import pandas as pd
import numpy as np

data_train = pd.read_csv('heart_train.data')
data_test = pd.read_csv('heart_test.data')

data_train.columns = ['Y', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12', 'F13', 'F14', 'F15', 'F16', 'F17', 'F18', 'F19', 'F20', 'F21', 'F22']
data_test.columns = ['Y', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12', 'F13', 'F14', 'F15', 'F16', 'F17', 'F18', 'F19', 'F20', 'F21', 'F22']

##########################################################################################################
################################# DECISION TREE IMPLEMENTATION ###########################################
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
    
    def __init__(self, data):
        self.data = data
        self.root = None
        self.training_error = None
        
    def classify(self):
        node = Node(self.data, None)
        self.root = node 
        return self.build_tree(node)
        
    def best_attribute(self, node):
        data = node.data
        M, N = data.shape;
        
        minimum_error = 1
        best_attr = None
        for attr in data.columns:
            if attr == 'Y' or attr == 'W':
                continue
            
            A_0p_e = A_1p_e = 0
            attr_values = data[attr].unique()    
            for attr_value in attr_values:
                split = data[data[attr] == attr_value]
                
                W_p = (split[split['Y'] == 1]['W']).sum()
                W_e = (split[split['Y'] == 0]['W']).sum()
                
                if attr_value == 0:                
                    A_0p_e = A_0p_e + W_e
                    A_1p_e = A_1p_e + W_p
                elif attr_value == 1:
                    A_0p_e = A_0p_e + W_p
                    A_1p_e = A_1p_e + W_e
            
            error = min(A_0p_e, A_1p_e)
            #print('ATTR, error ', attr, error)
            if error < minimum_error:
                minimum_error = error
                best_attr = attr
                is_0p = A_0p_e < A_1p_e
                
        return (best_attr, minimum_error, is_0p)
        
    def build_tree(self, node):        
        data = node.data
        (attr, error, is_0p) = self.best_attribute(node)
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
                child.decision = 0
            elif attr_value == 0 and not is_0p:
                child.decision = 0
            elif attr_value == 1 and not is_0p:
                child.decision = 1
                
        return error
    
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
################################# BAGGING IMPLEMENTATION ###########################################
##########################################################################################################

def bagging(data_train, bootstrap_samples):
    classifiers = []
    M,N = data_train.shape
    data_train['W'] = (np.ones(M)*(1.0/M)).reshape(M,1)
    for i in range(bootstrap_samples):            
        (train_size, attributes) = data_train.shape
        bootstrapped_data = data_train.iloc[np.unique(np.random.randint(0, M, size= M))]
        #print(bootstrapped_data)
        classifier = DT(bootstrapped_data)
        classifier.classify()
        classifiers.append(classifier)
        print('BAGGED SAMPLE : ', i+1, ', SPLIT ATTRIBUTE : ', classifier.root.attr)
    
    return classifiers

def predict(data_test, classifiers):    
    M, N = data_test.shape
    Y = data_test['Y'].values.reshape(M,1)
    Y_pred = np.zeros(M).reshape(M,1)
    
    samples = len(classifiers)
    
    for i in range(samples):
        Y_pred = Y_pred + np.array(classifiers[i].predict_dataset(data_test)).reshape(M,1)
    
    Y_pred[Y_pred < (samples/2)] = 0
    Y_pred[Y_pred >= (samples/2)] = 1
    
    #print('Y_pred ', Y_pred, Y)
    
    misclassifications = sum(abs(Y-Y_pred))
    
    return (1.0 - misclassifications/M ) * 100

classifiers = bagging(data_train, bootstrap_samples=20)
training_accuracy = predict(data_train, classifiers)
print('ACCURACY ON TRAINING SET ', training_accuracy)
test_accuracy = predict(data_test, classifiers)
print('ACCURACY ON TEST SET : ', test_accuracy)       

    
    
