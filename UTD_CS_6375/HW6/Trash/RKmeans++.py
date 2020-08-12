# -*- coding: utf-8 -*-
"""
Created on Sun May 10 12:42:11 2020

@author: ROHITH PEDDI
"""


import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

Train_data = np.array(pd.read_csv('leaf.data',header = None))
cols = Train_data.shape[1] - 1

def splitData(data):
    data = data[:,1:data.shape[1]]
    return data

def preprocessData(data):
    rows, cols = data.shape
    for i in range(cols):
        mean = np.mean(data[:, i])
        std = np.std(data[:, i])
        data[:, i] = (data[:, i]-mean)/std
    return data
        
    
    
def getClusterCenters(data, k):
    rows, cols = data.shape
    centers = np.zeros((k, cols))
    r = np.random.choice(rows, 1) #Initial Choice
    centers[0, :] = data[r, :]
    k_center = 1
    while k_center < k:
        pd = [] #pd represents probability distribution
        dist_sum = 0
        for i in range(rows):
            max_dist = 1000
            for j in range(k_center):
                dist = np.linalg.norm(data[i] - centers[j]) ** 2
                if dist < max_dist:
                    max_dist = dist
            d = max_dist*max_dist
            dist_sum += d
            pd.append(d)
        for i in range(rows):
            pd[i] = pd[i]/dist_sum
        r = np.random.choice(rows, 1, p=pd) 
        centers[k_center, :] = data[r, :]
        k_center = k_center + 1
    return centers

    
def clusters_formation(labels, data, total_clusters):
    clusters = []  #Initilaizing the Clusters 
    m = total_clusters
    for i in range(m):   #Initilaizing each Cluster Center 
        clusters.append([])
    n = len(data)
    for i in range(n):
        clusters[labels[i]].append(data[i])
    return clusters
    

def loss(clusters, centers):
    n = len(centers)
    loss = 0
    
    for i in range(n): #for each cluster
        cluster_center = centers[i]
        cluster = clusters[i]
        for j in cluster:
            k = np.linalg.norm(cluster_center-j)
            loss += k**2
    return loss    



data = splitData(Train_data) #Split Data sepearting the class labels
data = preprocessData(data) #Preprocessing the Data

k = [12, 18, 24, 36, 42]

obj_loss_list = []
for i in k:
    obj = []
    for j in range(20):
        cluster_centers = getClusterCenters(data, i)
        clustering = KMeans(n_clusters=i , init = cluster_centers).fit(data)
        clusters = clusters_formation(clustering.labels_, data, i)
        l = loss(clusters, clustering.cluster_centers_)
        obj.append(l)
    obj_loss_list.append(obj)
    print('The mean and variance of the kmeans objective for k = ',i,'is',np.mean(obj),'and ',np.var(obj))




    
    