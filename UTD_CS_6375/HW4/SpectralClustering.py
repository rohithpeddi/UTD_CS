# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

circs = pd.read_csv('circs.csv').values.transpose()

def plot_data(X, y_km, kmeans, type):
    
    print('-------------------------PLOTTING CLASSIFIED', type , ' --------------------------')
    
    plt.scatter(
        X[y_km == 0, 0], X[y_km == 0, 1],
        s=50, c='lightgreen',
        marker='s', edgecolor='black',
        label='cluster 1'
    )

    plt.scatter(
        X[y_km == 1, 0], X[y_km == 1, 1],
        s=50, c='orange',
        marker='o', edgecolor='black',
        label='cluster 2'
    )
    
    # plot the centroids
    plt.scatter(
        kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1],
        s=250, marker='*',
        c='red', edgecolor='black',
        label='centroids'
    )
    
    plt.legend(scatterpoints=1)
    plt.grid()
    plt.show()
    plt.label = type
    #plt.savefig(type)

def similarity_matrix(X, sigma):
    M, N = X.shape
    A = np.empty((M,M))
    for i in range(M):
        for j in range(M):
            distance = np.linalg.norm(X[i]-X[j])
            A[i][j] = A[j][i] = (-1/(2*(sigma**2)))* (distance**2)
    A = np.exp(A)    
    return A

def spectral_clusters(A, k):
    M, N = A.shape
    
    D = np.diag(np.sum(A, axis=1))    
    L = D - A
    
    eigen_values, eigen_vectors = np.linalg.eigh(L)
    
    # Find k smallest eigen values
    idx = np.argpartition(eigen_values, k)
    
    # Construct matrix V (n,k) with eigen vectors corresponding to k smallest values
    V = eigen_vectors[:, idx[:k]]
    
    # Kmeans for rows of the matrix and find corresponding clusters 
    # Assign final clusters to the dataset
    kmeans = KMeans(n_clusters=k, random_state=0)
    y_km = kmeans.fit_predict(V)
    
    return (kmeans, y_km)

def kmeans_clusters(X, k):
    kmeans = KMeans(n_clusters=k, random_state=0)
    y_km = kmeans.fit_predict(X)
    plot_data(X, y_km, kmeans, ' KMEANS CLUSTERS ')
    return

def spectral_clustering(X, k):    
    for i in range(-2, 5):
        sigma = 10**i
        A = similarity_matrix(X, sigma)
        (kmeans, y_km) = spectral_clusters(A, k)
        plot_data(X, y_km, kmeans, 'SPECTRAL CLUSTERING SIGMA ' + str(sigma))
    return

def comparison(X, k):
    #print('COMPUTING KMEANS CLUSTERS ON THE DATA')
    kmeans_clusters(X, k)
    #print('COMPUTING SPECTRAL CLUSTERS ON THE DATA')
    spectral_clustering(X, k)
    return

comparison(circs, 2)
