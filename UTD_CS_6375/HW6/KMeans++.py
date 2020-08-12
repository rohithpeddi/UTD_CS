# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 00:24:39 2020

@author: ROHITH PEDDI
"""

import pandas as pd
import numpy as np

data_train = pd.read_csv('leaf.data', header = None).values

###################################################################################
#######################              KMEANS++              ########################
###################################################################################

class KMeansPlusPlus(object):
    
    def __init__(self, n_clusters, tol, max_iter):
        self.n_clusters = n_clusters
        self.tol = tol
        self.max_iter = max_iter      
        self.cluster_centers = None
        self.labels = None
        self.inertia = None
        self.initial_cluster_centers = None
        
    def normalize(self, X):
        NUM, DIM = X.shape    
        X_mean = X.sum(axis=0)/NUM
        X_sd = np.sqrt( ((X - X_mean)**2).sum(axis=0)/NUM )    
        X_norm = (X-X_mean)/X_sd
        return X_norm
    
    def get_initial_centers(self, X):
        M,N = X.shape
    
        # Pick a random point
        cluster_centers = []
        initial_point = (X[np.random.randint(0, M),:]).reshape(1, -1)
        cluster_centers.append(initial_point)
        
        # Run the loop for k-1 times
        for k in range(self.n_clusters-1):    
            # Find distances of each point from the nearest point
            distances = []
            for i in range(M):
                X_i = X[i]
                min_distance = 1e+20
                for j in range(len(cluster_centers)):
                    current_distance = np.sum( (X_i-cluster_centers[j])**2 )
                    if current_distance < min_distance:
                        min_distance = current_distance                
                distances.append(min_distance)
                
            # Normalize distance measures such that sum of them is unity
            distances = np.array(distances).reshape(1, M)
            distances_sum = np.sum(distances)
            distances = distances/distances_sum      
            
            # Associate distance with probability measure of picking other points
            probabilities = distances.flatten().tolist()
            sampled_choice = np.random.choice(list(range(0, M)), 1, p=probabilities)
            
            # Pick new points with corresponding probabilities
            new_cluster_center = X[sampled_choice]
            cluster_centers.append(new_cluster_center)    
        
        return np.array(cluster_centers).reshape(self.n_clusters, N)
    
    def update_cluster_centers(self, X, labels, previous_centers):
        cluster_centers = []
        for i in range(self.n_clusters):
            cluster_i = X[np.where(labels == i)[0]]
            M_c_i, N_c_i = cluster_i.shape
            center_i = previous_centers[i] if M_c_i == 0 else np.mean(cluster_i, axis=0)
            cluster_centers.append(center_i)
        return cluster_centers
    
    def update_labels(self, X, cluster_centers):
        M, N = X.shape
        labels = []
        for i in range(M):
            X_i = X[i]
            best_k = None
            minimum_distance = 1e+100
            for j in range(self.n_clusters):
                current_distance = np.dot(cluster_centers[j]-X_i, cluster_centers[j]-X_i)
                if current_distance < minimum_distance:
                    minimum_distance = current_distance
                    best_k = j
            labels.append(best_k)
        
        return np.array(labels).reshape(M, 1)
    
    def compute_inertia(self, X, labels, cluster_centers):
        inertia = 0
        for i in range(self.n_clusters):
            cluster_i = X[np.where(labels == i)[0]]
            M_c_i, N_c_i = cluster_i.shape
            if M_c_i == 0:
                continue
            else:
                inter_cluster_distance = cluster_i - cluster_centers[i]
                inertia = inertia + np.sum(inter_cluster_distance**2)
                
        return inertia

    def fit(self, X):            
        X = self.normalize(X)
        
        M, N = X.shape          
        cluster_centers = self.get_initial_centers(X)
        labels = self.update_labels(X, cluster_centers)
        inertia = self.compute_inertia(X, labels, cluster_centers)
        print('INITIALIZING COMPLETE')
        
        iterations = 0
        isLocalOptimum = False
        while not isLocalOptimum:
            print('-------------------------- ITERATION ', iterations ,'---------------------------')          
            print('PREVIOUS INERTIA ', inertia)
            
            labels = self.update_labels(X, cluster_centers)
            cluster_centers = self.update_cluster_centers(X, labels, cluster_centers)
            
            current_inertia = self.compute_inertia(X, labels, cluster_centers)
            print(current_inertia)
            
            if abs(inertia-current_inertia) < self.tol or iterations > self.max_iter:
                isLocalOptimum = True
                print(labels.reshape(1,-1))
                self.labels = labels
                self.cluster_centers = cluster_centers
                self.inertia = inertia

                
            inertia = current_inertia
            iterations = iterations+1
            
            print('----------------------------------------------------------------')    
    
M, N = data_train.shape
cluster_centers = data_train[:, 0]
X = data_train[:, 1:N]

k_list = [12, 18, 24, 36, 42]
tol = 1e-17
max_iter = 1e+4

inertia_matrix = np.empty((20, 5))

for i in range(20):
    for j in range(len(k_list)):
        print('#############################################################################')
        k = k_list[j]
        print('RUNNING KMEANS FOR ', k)
        kmeans = KMeansPlusPlus(k, tol, max_iter)
        kmeans.fit(X)
        inertia_matrix[i][j] = kmeans.inertia
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    