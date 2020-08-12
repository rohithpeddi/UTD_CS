# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 21:38:08 2020

@author: ROHITH PEDDI
"""

import numpy as np
import pandas as pd
import math
from sklearn.metrics import adjusted_rand_score
from sklearn.metrics import fowlkes_mallows_score


def logLikelihood(data, mean, covariance, lambda1, k, m): # Log Likelihood 
    log = 0
    for i in range(len(data)):
        sum1 = 0
        for j in range(k):
            sum1 += lambda1[j] * guassian(data[i], mean[j], covariance[j], m)
        log += np.log(sum1)
    return log

def gmmPred(data, mean, covariance, lambda1, k, m):
    pred = []
    for i in range(len(data)):
        best_likelihood = None
        best_cluster = None
        for j in range(k):
            likelihood = lambda1[j] * guassian(data[i], mean[j], covariance[j], m)
            if best_likelihood is None or best_likelihood <= likelihood:
                best_likelihood = likelihood
                best_cluster = j
        pred.append(best_cluster)
    return pred

def preprocessData(data): #Preprocessing Data
    rows, cols = data.shape
    for i in range(cols):
        mean = np.mean(data[:, i])
        std = np.std(data[:, i])
        data[:, i] = (data[:, i]-mean)/std
    return data

def guassian(row, mean, covariance, m): # Multivariate Gaussian
    diff_data_mean = np.array(row - mean).reshape(1, m)
    exp = np.exp(-0.5 * np.dot(np.dot(diff_data_mean, np.linalg.inv(covariance)), diff_data_mean.T))
    return (1 / np.sqrt(((2 * math.pi) ** m) * np.linalg.det(covariance))) * exp


train_data = np.array(pd.read_csv('leaf.data',header = None)) #Train data
trainLength = len(train_data)
train_features = train_data[:, 0]
train_data = train_data[:, 1:]
cols = len(train_data[0])
scaledData = preprocessData(train_data) #Scaling data

kArray = [12, 18, 24, 36, 42] # K array

# Get GMM objective loss array and compute mean and variance
lossArray = []

meanArray = []
covarianceArray = []
lambdaArray = []
# For each K
for k in kArray:
    print('K-value',k)
    for i in range(20): #20 random Intializations
        print("Iter",i)
        centers = np.empty((k, cols), dtype=np.float64)
        for j in range(k):
            centers[j] = np.array(np.random.choice(np.arange(-3, 4, 1), cols)).reshape(1, cols)
        cov_matrix_arr = np.empty((k, cols, cols))
        for j in range(k):
            cov_matrix_arr[j] = np.identity(n=cols, dtype=np.float64)

        lambda_arr = np.empty((k, 1), dtype=np.float64)
        for j in range(k):
            lambda_arr[j] = 1/k

        logLikelihoodVal = logLikelihood(scaledData, centers, cov_matrix_arr, lambda_arr, k, cols)
        iteration_counter = 1
        while True:
            #E Step
            q_array = np.empty((trainLength, k), dtype=np.float64)
            for x in range(trainLength):
                den_sum = 0
                for k_val in range(k):
                    q_array[x, k_val] = lambda_arr[k_val] * guassian(scaledData[x], centers[k_val], cov_matrix_arr[k_val], cols)
                    den_sum += q_array[x, k_val]

                q_array[x] = q_array[x] / den_sum
            #M Step
            for k_val in range(k):
                num_total = 0
                den_total = 0
                for m in range(trainLength):
                    num_total += q_array[m, k_val] * scaledData[m]
                    den_total += q_array[m, k_val]
                centers[k_val] = num_total / den_total

            for k_val in range(k):
                num_total = 0.0
                den_total = 0.0

                for m in range(trainLength):
                    diff_vector = scaledData[m] - centers[k_val]
                    diff_vector = np.array(diff_vector).reshape((1, cols))
                    num_total += q_array[m, k_val] * np.dot(diff_vector.T, diff_vector)
                    den_total += q_array[m, k_val]
                cov_matrix_arr[k_val] = num_total / den_total
                cov_matrix_arr[k_val] += np.identity(n=cols)

            for k_val in range(k):
                num_total = 0
                for m in range(trainLength):
                    num_total += q_array[m, k_val]

            lambda_arr[k_val] = num_total / trainLength

            prevLog = logLikelihoodVal
            logLikelihoodVal = logLikelihood(scaledData, centers, cov_matrix_arr, lambda_arr, k, cols)
            if prevLog >= logLikelihoodVal:             # Convergence Check
                lossArray.append(logLikelihoodVal)
                meanArray.append(centers)
                covarianceArray.append(cov_matrix_arr)
                lambdaArray.append(lambda_arr)
                break

index = 0            # Mean and variance of GMM objective    
while index < 5:
    k = index * 20
    print("The mean and Variance of the GMM Objective for k =",kArray[index],"is", np.mean(lossArray[k:k+20]), "and:", np.var(lossArray[k:k+20]))
    index += 1

"""
Using 2 metrics to compare clusters against true labels 
"""
adjRand = 0
fms = 0
temp_data = np.append(scaledData, np.array(train_features - 1).reshape((trainLength, 1)), axis=1)
for i in range(20):
    predict_array = gmmPred(scaledData, meanArray[60+i], covarianceArray[60+i], lambdaArray[60+i], 36, cols)
    adjRand += adjusted_rand_score(train_data[:, 0], predict_array) #Adjusted Rand Score
    fms += fowlkes_mallows_score(train_data[:, 0], predict_array) #Fowlkes Mallows Score

print("Adjusted Rand Index of the GMM model with k: 36 is", adjRand/20)
print("Fowkes Mallows Score of the GMM model with k: 36 is", fms/20)