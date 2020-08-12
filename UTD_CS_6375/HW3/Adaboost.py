# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 21:44:08 2020

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
            
            A_0pos_error = A_1pos_error = 0
            attr_values = data[attr].unique()    
            for attr_value in attr_values:
                split = data[data[attr] == attr_value]
                
                W_p = (split[split['Y'] == 1]['W']).sum()
                W_n = (split[split['Y'] == -1]['W']).sum()
                
                if attr_value == 0:                
                    A_0pos_error = A_0pos_error + W_n
                    A_1pos_error = A_1pos_error + W_p
                elif attr_value == 1:
                    A_0pos_error = A_0pos_error + W_p
                    A_1pos_error = A_1pos_error + W_n
            
            error = min(A_0pos_error, A_1pos_error)
            if error < minimum_error:
                minimum_error = error
                best_attr = attr
                is_0p = A_0pos_error < A_1pos_error
                
        All_pos_error = data[data['Y'] == -1]['W'].sum()
        All_neg_error = data[data['Y'] == 1]['W'].sum()
        
        All_pos = All_neg = False
        if All_pos_error < minimum_error:
            minimum_error = All_pos_error
            All_pos = True
            All_neg = False
            
        if All_neg_error < minimum_error:
            minimum_error = All_neg_error
            All_pos = False
            All_neg = True
                
        return (best_attr, minimum_error, is_0p, All_pos, All_neg)
        
    def build_tree(self, node):        
        data = node.data
        (attr, error, is_0p, All_pos, All_neg) = self.best_attribute(node)
        
        if All_pos:
            node.decision = 1
            node.attr = 'POSITIVE'
            return error
        
        if All_neg:
            node.decision = -1
            node.attr = 'NEGATIVE'
            return error
        
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
################################# ADABOOST IMPLEMENTATION ###########################################
##########################################################################################################

def update_weights(data, classifier, alpha, error):
    normalizing_constant = (2.0)*(np.sqrt(error*(1-error)))
    
    Y = data['Y']
    Y_pred = classifier.predict_dataset(data)
    W = data['W']
    
    W_updated = ( (W)*(np.exp(-1.0 * Y*Y_pred*alpha))/normalizing_constant )
    data['W'] = W_updated
    
    return data


def adaboost(data_train, iterations):
    # Initialize all weights to (1/M)
    M, N = data_train.shape;
    data = data_train
    data['W'] = (np.ones(M)*(1.0/M)).reshape(M,1)
    
    classifiers = []
    alphas = []
    
    for i in range(iterations):
        # Select the classifier that has minimizes weighted misclassification error
        classifier = DT(data)
        error = classifier.classify()
        
        # Compute alpha
        alpha = (0.5)*(np.log((1-error)/error))
        
        # Update weights
        data = update_weights(data, classifier, alpha, error)
        
        alphas.append(alpha)
        classifiers.append(classifier)
        print('ATTR : ', i, classifier.root.attr)
        
    return (alphas, classifiers)

def predict(data, alphas, classifiers):
    
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
    
(alphas, classifiers) = adaboost(data_train, iterations=20)
training_accuracy = predict(data_train, alphas, classifiers)
print('ACCURACY ON TRAINING SET', training_accuracy)
test_accuracy = predict(data_test, alphas, classifiers)
print('ACCURACY ON TEST SET : ', test_accuracy)

        
    
