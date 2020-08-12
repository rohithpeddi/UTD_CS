# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 23:43:21 2020

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

#1. Attr1 - 0 - +ve - 1 -ve
#2. Attr1 - 0 - -ve - 1 +ve
#3. Attr1 - 0 - +ve - 1 Split - Attr2 - 0 - +ve - 1 - -ve
#4. Attr1 - 0 - +ve - 1 Split - Attr2 - 0 - -ve - 1 - +ve        
#5. Attr1 - 0 - -ve - 1 Split - Attr2 - 0 - +ve - 1 - -ve        
#6. Attr1 - 0 - -ve - 1 Split - Attr2 - 0 - -ve - 1 - +ve        
#7. Attr1 - 0 Split - Attr2 - 0 - +ve - 1 - -ve - 1 - +ve        
#8. Attr1 - 0 Split - Attr2 - 0 - +ve - 1 - -ve - 1 - -ve        
#9. Attr1 - 0 Split - Attr2 - 0 - -ve - 1 - +ve - 1 - +ve        
#10. Attr1 - 0 Split - Attr2 - 0 - -ve - 1 - +ve - 1 - -ve


class Node(object):    
    
    def __init__(self, data, parent_attr_value, parent_attr, decision, attr):
        self.data = data
        self.children = []
        self.attr = attr
        self.decision = decision
        self.parent_attr = parent_attr
        self.parent_attr_value = parent_attr_value

class DT(object):
    
    classifiers = []    
    pos_node = Node(None, None, None, 1, 'POSITIVE')    
    neg_node = Node(None, None, None, -1, 'NEGATIVE')
    
    classifiers.append(pos_node)
    classifiers.append(neg_node)
    
    for attr in data_train.columns:
        if attr == 'Y' or attr == 'W':
            continue
        
        L0 = 1
        L1 = -1
        for i in range(2):        
            left_child = Node(None, 0, attr, L0, None)
            right_child = Node(None, 1, attr, L1, None)
            
            root = Node(None, None, None, None, attr)
            root.children.append(left_child)
            root.children.append(right_child)
            
            classifiers.append(root)
            
            L0 = -1*L0
            L1 = -1*L1        
        
        # RIGHT SPLIT
        L0 = 1
        L1A0 = 1
        L1A1 = -1
        for attr2 in data_train.columns:
            if attr2 == attr or attr2 == 'Y' or attr2 == 'W':
                continue
            
            for j in range(4): # FOR EVERY ATTR2 4 DIFFERENT TREES WITH RIGHT SPLIT
                root = Node(None, None, None, None, attr)
                
                left_child = Node(None, 0, attr, L0, None)                        
                right_child = Node(None, 1, attr, None, attr2)
                
                right_left_child = Node(None, 0, attr2, L1A0, None)
                right_right_child = Node(None, 1, attr2, L1A1, None)

                right_child.children.append(right_left_child)
                right_child.children.append(right_right_child)                        
                
                root.children.append(left_child)
                root.children.append(right_child)
                
                classifiers.append(root)
                
                L1A0 = -1*L1A0
                L1A1 = -1*L1A1
                if j%2 == 1:
                    L0 = -1*L0
            
        # LEFT SPLIT
        L0A0 = 1
        L0A1 = -1
        L1 = 1
        for attr2 in data_train.columns:
            if attr2 == attr or attr2 == 'Y' or attr2 == 'W':
                continue
            
            for j in range(4): # FOR EVERY ATTR2 4 DIFFERENT TREES WITH RIGHT SPLIT
                root = Node(None, None, None, None, attr)
                
                left_child = Node(None, 0, attr, None, attr2)                        
                right_child = Node(None, 1, attr, L1, None)
                
                left_left_child = Node(None, 0, attr2, L0A0, None)
                left_right_child = Node(None, 1, attr2, L0A1, None)

                left_child.children.append(left_left_child)
                left_child.children.append(left_right_child)                        
                
                root.children.append(left_child)
                root.children.append(right_child)
                
                classifiers.append(root)
                
                L0A0 = -1*L0A0
                L0A1 = -1*L0A1
                if j%2 == 1:
                    L1 = -1*L1
                        
    
    def __init__(self, data):
        self.data = data
        self.root = None
        self.training_error = None
        
    def classify(self):
        data = self.data
        (classifier, error) = self.best_classifier(data)
        self.root = classifier
        return error
    
    def best_classifier(self, data):
        minimum_error = 10000000000000000        
        M, N = data.shape        
        best_classifier = None
        Y = data['Y'].values.reshape(M,1)
        W = data['W'].values.reshape(M,1)
        
        for classifier in self.classifiers:
            #print('CLASSIFIER ', classifier.attr)
            Y_pred = np.array(self.predict_dataset(data, classifier)).reshape(M,1)            
            error = W[abs(Y-Y_pred) > 0].sum()
            #print('CLASSIFIER ', classifier.attr, ', error ', error, ', min error ', minimum_error)
            if error < minimum_error:
                minimum_error = error
                best_classifier = classifier
                
        return (best_classifier, minimum_error)            
        
    def predict_dataset(self, data, classifier):
        Y_pred = []
        for i in range(0, len(data)):
            #print('PREDICT CLASSIFIER ', classifier.attr)
            prediction = self.predict(classifier, data.iloc[i])
            Y_pred.append(prediction)
        return Y_pred  
    
    def predict_data(self, data):    
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
            #print(child.parent_attr_value, attr, len(node.children))
            if child.parent_attr_value == data_point[attr]:
                break              
        #print('F ', child.attr, child.decision)
        return self.predict(child, data_point)       
    
    def print_structure(self):
        node = self.root
        print('ROOT ', node.attr)
        
        if node.decision is not None:
            print(node.decision)
        else :
            left_child = node.children[0]
            right_child = node.children[1]
            
            print('LEFT ', left_child.attr, left_child.decision, left_child.parent_attr_value, left_child.parent_attr)
            print('RIGHT ', right_child.attr, right_child.decision, right_child.parent_attr_value, right_child.parent_attr)
            
            if left_child.decision is None:
                left_left_child = left_child.children[0]
                left_right_child = left_child.children[1]
                
                print('LEFT LEFT', left_left_child.attr, left_left_child.decision, left_left_child.parent_attr_value, left_left_child.parent_attr)
                print('LEFT RIGHT ', left_right_child.attr, left_right_child.decision, left_right_child.parent_attr_value, left_right_child.parent_attr)
           
            if right_child.decision is None:
                right_left_child = right_child.children[0]
                right_right_child = right_child.children[1]
                
                print('RIGHT LEFT', right_left_child.attr, right_left_child.decision, right_left_child.parent_attr_value, right_left_child.parent_attr)
                print('RIGHT RIGHT ', right_right_child.attr, right_right_child.decision, right_right_child.parent_attr_value, right_right_child.parent_attr)
           

##########################################################################################################
################################# ADABOOST IMPLEMENTATION ###########################################
##########################################################################################################

def update_weights(data, classifier, alpha, error):
    normalizing_constant = (2.0)*(np.sqrt(error*(1-error)))
    
    Y = data['Y']
    Y_pred = classifier.predict_data(data)
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
    training_accuracies = []
    test_accuracies = []
    
    for i in range(iterations):
        print('------------------------------------------------------------')
        print('ITERATION ', i)
        # Select the classifier that has minimizes weighted misclassification error
        classifier = DT(data)
        error = classifier.classify()
        
        # Compute alpha
        alpha = (0.5)*(np.log((1-error)/error))
        print('ERROR ', error)
        print('ALPHA ', alpha)
        
        # Update weights
        data = update_weights(data, classifier, alpha, error)
        
        alphas.append(alpha)
        classifiers.append(classifier)
        
        training_accuracy = predict(data_train, alphas, classifiers)
        print('ACCURACY ON TRAINING SET', training_accuracy)
        test_accuracy = predict(data_test, alphas, classifiers)
        print('ACCURACY ON TEST SET : ', test_accuracy)
        
        training_accuracies.append(training_accuracy)
        test_accuracies.append(test_accuracy)
        
        print('ATTR : ', i, classifier.root.attr)
        classifier.print_structure()        
        
        print('------------------------------------------------------------')
        
    return (alphas, classifiers, training_accuracies, test_accuracies)

def predict(data, alphas, classifiers):
    
    M, N = data.shape
    Y = data['Y'].values.reshape(M,1)
    Y_pred = np.zeros(M).reshape(M,1)
    
    N_c = len(classifiers)
    
    for i in range(N_c):
        alpha = alphas[i]
        Y_pred = Y_pred + alpha*(np.array(classifiers[i].predict_data(data)).reshape(M,1))
        
    
    Y_pred[Y_pred < 0] = -1
    Y_pred[Y_pred >= 0] = 1
    #print(Y-Y_pred)
    
    misclassification = sum(abs(Y-Y_pred))/2
    
    return (1.0 - misclassification/M ) * 100
    
(alphas, classifiers, training_accuracies, test_accuracies) = adaboost(data_train, iterations=10)
training_accuracy = predict(data_train, alphas, classifiers)
print('ACCURACY ON TRAINING SET', training_accuracy)
test_accuracy = predict(data_test, alphas, classifiers)
print('ACCURACY ON TEST SET : ', test_accuracy)

#plt.plot(Y, training_accuracies)
#plt.plot(Y, test_accuracies)
#plt.show()