# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 00:02:13 2020

@author: ROHITH PEDDI
"""

import numpy as np
import math
from sklearn.cluster import KMeans
from sklearn.cluster import SpectralClustering
import matplotlib.pyplot as plt
import skimage.io as sk

def cluster_loss(clusters, centers, k):
    loss = 0
    for i in range(k):
        center = centers[i]
        cluster = clusters[i]
        for data_point in cluster:
            loss = loss + (np.linalg.norm(data_point-center))**2
    return loss

def similarity_matrix(X, sigma):
    M, N = X.shape
    A = np.zeros((M,M))
    #sigma2 = 0.05
    constant = -2.0*(sigma**2)
    constant = (1.0/constant)
    for i in range(M):
        for j in range(i+1):
            if i==j:
                A[i][j] = 1
            else :
                distance = X[i]-X[j]
                val = (constant)* (distance**2)
                A[i][j] = A[j][i] = np.exp(val)
    print('FINISHED COMPUTING SIMILARITY MATRIX for sigma ', sigma)
    return A

def spectral_clusters(A, k):
    M, N = A.shape
    
    D = np.diag(np.sum(A, axis=1))    
    L = D - A
    
    eigen_values, eigen_vectors = np.linalg.eigh(L)
    
    # Find k smallest eigen values
    idx = eigen_values.argsort()[0:k]
    
    # Construct matrix V (n,k) with eigen vectors corresponding to k smallest values
    V = eigen_vectors[:, idx]
    
    # Kmeans for rows of the matrix and find corresponding clusters 
    # Assign final clusters to the dataset
    kmeans = KMeans(n_clusters=k, random_state=0)
    y_km = kmeans.fit_predict(V)
    y_km = y_km*255
    
    print('FINISHED COMPUTING SPECTRAL CLUSTERING')
    return (kmeans, y_km)

def kmeans_clusters(X, k):
    kmeans = KMeans(n_clusters=k, random_state=0)
    y_km = kmeans.fit_predict(X)
    (kmeans, y_km) = kmeans_clusters(data, K)
    image_labels = np.reshape(y_km, (75, 100))
    sk.imshow(image_labels)
    return (kmeans, y_km)

def spectral_clustering(X, k):    
    for i in range(56, 65):
        sigma = i/1000
        print('------------------------------------------------------------------------------')
        print('CALCULATING SPECTRAL CLUSTERING FOR k ', k, ', sigma ', sigma)        
        A = similarity_matrix(X, sigma)
        (spectral_kmeans, spectral_y_km) = spectral_clusters(A, k)
        #image_labels = np.array(spectral_y_km).astype(np.float)
        image_labels = np.reshape(spectral_y_km, (75, 100))
        #sk.imshow(image_labels)
        name = 'Actual_Spectral' + str(sigma) + '.jpg'
        sk.imsave(name, image_labels)
    return 

def scikit_spectral(X, k):
    clustering = SpectralClustering(n_clusters=2, assign_labels="discretize", random_state=0).fit(X)
    spectral_y_km = clustering.labels_
    image_labels = np.reshape(spectral_y_km, (75, 100))
    sk.imshow(image_labels)
    name = 'Scikit_Spectral.jpg'
    sk.imsave(name, image_labels)
    return clustering

def normalize(X):    
    M,N = X.shape    
    X_mean = X.sum(axis=0)/M
    X_sd = np.sqrt( ((X - X_mean)**2).sum(axis=0)/M )    
    return (((X - X_mean) / X_sd), X_mean, X_sd)

#Converting a grayscale image into a list of pixel values
data = plt.imread("bw.jpg")
data = data.reshape(-1,1)

(data, data_mean, data_sd) = normalize(data)
K = 2 

#scikit_spectral_clustering = scikit_spectral(data, K)
spectral_clustering(data, K)
#kmeans_clusters(data, K)




