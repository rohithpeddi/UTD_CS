# -*- coding: utf-8 -*-
"""
Created on Sun May 10 17:29:41 2020

@author: ROHITH PEDDI
"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

data_train = pd.read_csv('leaf.data', header = None).values

M, N_c = data_train.shape
cluster_centers_actual = data_train[:, 0]
X = data_train[:, 1:N_c]

#k_list = [12, 18, 24, 36, 42]
k_list = [36]
tol = 1e-17
max_iter = 1e+4
N = N_c-1

###################################################################################
#######################                KMEANS            ########################
###################################################################################

def get_vanilla_cluster_centers(n_clusters):
    cluster_centers = np.empty((n_clusters, N))
    for k in range(n_clusters):
        cluster_centers[k] = np.array(np.random.choice(np.arange(-3, 4, 1), N)).reshape(1, N)            
    return cluster_centers

def Vanilla_Kmeans():
    inertia_matrix = np.empty((20, 5))    
    for i in range(1):
        for j in range(len(k_list)):
            print('#############################################################################')
            n_clusters = k_list[j]
            print (n_clusters, ' CLUSTERS, ','ITERATION ', i)
            cluster_centers = get_vanilla_cluster_centers(n_clusters)
            kmeans = KMeans(n_clusters=n_clusters, init=cluster_centers, tol=tol, max_iter=max_iter, verbose=1, n_init=1).fit(X)
            predicted_cluster_labels = kmeans.labels_
            print(cluster_centers_actual)
            print(predicted_cluster_labels+1)            
            inertia_matrix[i][j] = kmeans.inertia_
    
    return inertia_matrix

vanilla_inertia_matrix = Vanilla_Kmeans()
vanilla_mean = np.mean(vanilla_inertia_matrix, axis = 0)
vanilla_var = np.var(vanilla_inertia_matrix, axis = 0)


###################################################################################
#######################                KMEANS++            ########################
###################################################################################

def get_kmeans_plus_plus_cluster_centers(n_clusters):
    # Pick a random point
    cluster_centers = []
    initial_point = (X[np.random.randint(0, M),:]).reshape(1, -1)
    cluster_centers.append(initial_point)
    
    # Run the loop for k-1 times
    for k in range(n_clusters-1):    
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
    
    return np.array(cluster_centers).reshape(n_clusters, N)

def Kmeans_plus_plus():
    kmeans_plus_plus_inertia_matrix = np.empty((20, 5))    
    for i in range(20):
        for j in range(len(k_list)):
            print('#############################################################################')
            n_clusters = k_list[j]
            print (n_clusters, ' CLUSTERS, ','ITERATION ', i)
            cluster_centers = get_kmeans_plus_plus_cluster_centers(n_clusters)
            kmeans = KMeans(n_clusters=n_clusters, init=cluster_centers, tol=tol, max_iter=max_iter, verbose=1, n_init=1).fit(X)
            predicted_cluster_labels = kmeans.labels_
            kmeans_plus_plus_inertia_matrix[i][j] = kmeans.inertia_
    
    return kmeans_plus_plus_inertia_matrix

#kmeans_plus_plus_inertia_matrix = Kmeans_plus_plus()
#kmeans_plus_plus_mean = np.mean(kmeans_plus_plus_inertia_matrix, axis = 0)
#kmeans_plus_plus_var = np.var(kmeans_plus_plus_inertia_matrix, axis = 0)