# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 20:40:07 2020

@author: ROHITH PEDDI
"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn import mixture

data_train = pd.read_csv('leaf.data', header = None).values

#k_list = [12, 18, 24, 36, 42]
k_list = [36]

M, N = data_train.shape
cluster_centers = data_train[:, 0]
data = data_train[:, 1:N]
    
def kmeans_random_check(X):
    for k in k_list:
        filename = str(k) + '_cluster_centers'
        cluster_centers = pd.read_csv(filename, header = None).values
        kmeans = KMeans(n_clusters=k, init=cluster_centers, tol=1e-10, max_iter=100000, verbose=1).fit(X)
        predicted_cluster_labels = kmeans.labels_
        print('--------------------------------------------------------------------------------')
        print(predicted_cluster_labels)
        print('--------------------------------------------------------------------------------')        

def kmeans_plus_plus_random_check(X):
    for k in k_list:
        print('#############################################################################')
        print('RUNNING KMEANS FOR ', k)
        kmeans = KMeans(n_clusters=k, init='k-means++', tol=1e-10, max_iter=100000, verbose=3).fit(X)
        predicted_cluster_labels = kmeans.labels_
        print('--------------------------------------------------------------------------------')
        print(predicted_cluster_labels)
        print('--------------------------------------------------------------------------------')  

def gmm_check(X):
    clf = mixture.GaussianMixture(n_components=36, covariance_type='full', verbose=3)
    clf.fit(X)
    print(clf.lower_bound_)
    
def generate_random_cluster_initializations():
    for cluster_length in k_list:
        filename = str(cluster_length) + '_cluster_centers'
        file = open(filename,"w+")
        
        for k in range(cluster_length):
            for n in range(N-1):
                c_k_n = np.random.uniform(-3,3)
                file.write(str(c_k_n))
                if n < N-2:
                    file.write(',')
            file.write('\n')
        file.close()
            
#generate_random_cluster_initializations()
print('########################################## KMEANS ##############################################')
#kmeans_random_check(data)
print('########################################## KMEANS++ ##############################################')
#kmeans_plus_plus_random_check(data)
print('########################################## GMM ##############################################')
gmm_check(data)