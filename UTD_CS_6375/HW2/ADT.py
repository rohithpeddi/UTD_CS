# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 10:06:17 2020

@author: ROHITH PEDDI
"""
import math
import pandas as pd

data_train = pd.read_csv('mush_train.data')
data_test = pd.read_csv('mush_test.data')

data_train.columns = ['category', 'cap-shape', 'cap-surface', 'cap-color', 'bruises', 'odor', 'gill-attachment', 'gill-spacing', 'gill-size', 'gill-color', 'stalk-shape', 'stalk-root', 'stalk-surface-above-ring', 'stalk-surface-below-ring', 'stalk-color-above-ring', 'stalk-color-below-ring', 'veil-type', 'veil-color', 'ring-number', 'ring-type', 'spore-print-color', 'population', 'habitat']
data_test.columns = ['category', 'cap-shape', 'cap-surface', 'cap-color', 'bruises', 'odor', 'gill-attachment', 'gill-spacing', 'gill-size', 'gill-color', 'stalk-shape', 'stalk-root', 'stalk-surface-above-ring', 'stalk-surface-below-ring', 'stalk-color-above-ring', 'stalk-color-below-ring', 'veil-type', 'veil-color', 'ring-number', 'ring-type', 'spore-print-color', 'population', 'habitat']

class Node(object):    
    def __init__(self, data, parent_attr_value):
        self.data = data
        self.children = []
        self.attr = None
        self.decision = None
        self.majority_vote = None
        self.information_gain = None
        self.parent_attr = None
        self.parent_attr_value = parent_attr_value

def entropy(data, y_attr):
    N_p = len(data[data[y_attr]=='p'])
    N_e = len(data[data[y_attr]=='e'])
    N = len(data)
    
    N_p_ad = N_p*1. / N*1.
    N_e_ad = N_e*1. / N*1.
    
    H_d = 0    
    if N_p_ad != 0:
        H_d = H_d +  -1.* math.log(N_p_ad**(N_p_ad), 2) 
    
    if N_e_ad != 0:
        H_d = H_d + -1.* math.log(N_e_ad**(N_e_ad), 2) 
        
    return (N, N_p, N_e, H_d)

def best_attribute(data, y_attr):
    N, N_p, N_e, H_d = entropy(data, y_attr)
    
    max_information_gain = 0
    best_attr = None
    
    for attr in data.columns:
        if attr == y_attr:
            continue
        
        H_d_attr = 0
        attr_values = data[attr].unique()        
        for attr_value in attr_values: 
            split = data[data[attr] == attr_value]
            split = split.drop(attr, 1)
            N_s, S_p, S_e, S_d = entropy(split, y_attr)            
            #print(attr, '-----------------', attr_value, N_s, S_p, S_e, S_d)
            H_d_attr = H_d_attr + (N_s*1. / N*1. )*(S_d)
        
        information_gain = H_d - H_d_attr
        if information_gain > max_information_gain:
            max_information_gain = information_gain
            best_attr = attr
        
        #print('ATTRIBUTE', attr, information_gain, H_d, H_d_attr, best_attr, max_information_gain)
        
    #print('BEST ATTRIBUTE', best_attr, max_information_gain, H_d_attr, attr_values)
    
    return (best_attr, max_information_gain)

def decision_tree(node, y_attr):
    data = node.data
    
    N, DIM = data.shape    
    N_p = len(data[data[y_attr]=='p'])
    N_e = len(data[data[y_attr]=='e'])
          
    if N_p > N_e:
        node.majority_vote = 'p'
        if N == N_p or DIM == 1:
            node.decision = 'p'
            return
    else:
        node.majority_vote = 'e'
        if N == N_e or DIM == 1:
            node.decision = 'e'
            return
    
    attr, information_gain = best_attribute(data, y_attr)
    
    node.attr = attr
    node.information_gain = information_gain
    
    # Fetch different values for the chosen attribute
    attr_values = data[attr].unique()
    
    # Split the data corresponding to each attribute chosen
    for attr_value in attr_values:
        split = data[data[attr] == attr_value]
        split = split.drop(attr, 1)
        child = Node(split, attr_value)
        child.parent_attr = attr
        node.children.append(child)
        decision_tree(child, y_attr)
        
def accuracy(predicted, data):
    return sum(predicted == data)*1. / len(data)*1.

counter = 0
def predict(node, data_point, level):
    global counter
    if node.decision is not None:
        return node.decision
    
    attr = node.attr    
    if attr not in data_point.index.values:    
        if node.majority_vote != data_point['p'] :
            counter = counter+1
            #print('NOT FOUND ', attr, node.majority_vote, data_point['p'], counter, level)    
        return node.majority_vote
    
    child = None
    for child in node.children:        
        if child.parent_attr_value == data_point[attr]:
            break      
    
    return predict(child, data_point, level+1)

predicted = []
def predict_dataset(node, data, y_attr):    
    for i in range(0, len(data)):
        prediction = predict(node, data.iloc[i], 0)
        #print(prediction, data[y_attr][i])
        predicted.append(prediction)
    
    print('ACCURACY ', accuracy(predicted, data[y_attr]))
    return 

def print_decision_tree(node, level):
    print(node.parent_attr,  node.parent_attr_value, node.attr, node.decision, len(node.data), level, node.information_gain)
    for child in node.children:
        print_decision_tree(child, level+1)

node  = Node(data_train, None)
decision_tree(node, 'category')
predict_dataset(node, data_test, 'category')
print_decision_tree(node, 0)
    
    
    
    
    