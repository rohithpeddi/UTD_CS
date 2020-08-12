# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 19:01:58 2020

@author: ROHITH PEDDI
"""
import pandas as pd
import numpy as np
import math

data_train = pd.read_csv('leaf.data', header = None).values

###################################################################################
##########################              GMM              ##########################
###################################################################################

class GMM(object):
    
    def __init__(self, n_clusters, tol, max_iter):
        self.n_clusters = n_clusters
        self.tol = tol
        self.max_iter = max_iter      
        self.cluster_centers = None
        self.labels = None
        self.inertia = None
        self.initial_cluster_centers = None
        
    def normalize(self, X):
        X_mean = np.mean(X, axis=0)
        X_sd = np.std(X, axis=0)
        return (X-X_mean)/X_sd
    
    def get_initial_centers(self, X):
        M,N = X.shape
        K = self.n_clusters
        
        # Pick a random point
        cluster_centers = []
        initial_point = X[np.random.choice(M)].reshape(1,N)
        cluster_centers.append(initial_point)
        
        # Run the loop for k-1 times
        for i in range(K-1):            
            # Find distances of each point from the nearest point
            distances = []
            for j in range(M):
                X_j = X[j]
                min_distance = 10000000
                for c in range(len(cluster_centers)):
                    X_j_c = X_j - cluster_centers[c]
                    current_distance = np.inner(X_j_c, X_j_c)
                    #current_distance = np.sum((data_point-cluster_centers[c])*(data_point-cluster_centers[c]))
                    if current_distance < min_distance:
                        min_distance = current_distance                
                distances.append(min_distance)
            
            # Normalize distance measures such that sum of them is unity
            distances = np.array(distances).reshape(1, M)
            distances_sum = np.sum(distances)
            distances = distances/distances_sum        
            
            # Associate distance with probability measure of picking other points
            probabilities = distances.flatten().tolist()
            choice = np.random.choice(list(range(0, M)), 1, p=probabilities)        
            
            # Pick new points with corresponding probabilities
            new_cluster_center = X[choice]
            cluster_centers.append(new_cluster_center) 
            
        return np.array(cluster_centers).reshape(K, N)

    def get_initial_parameters(self, X):
        M,N = X.shape
        K = self.n_clusters
        means = self.get_initial_centers(X)
        covariances = np.empty((K, N, N))
        for k in range(K):
            covariances[k] = np.eye(N)
        lambdas = np.ones((K,1))*(1/K)
        return means, covariances, lambdas
    
    def guassian(self, data_point, mean, covariance):
        N = len(mean)
        covariance_determinant = np.linalg.det(covariance)
        covariance_inverse = np.linalg.inv(covariance)

        if covariance_determinant == 0:
            print('COVARIANCE DETERMINANT ZERO!!!!')

        X_mean = (data_point-mean).reshape(1, N)
        exponential = np.exp(-0.5 * np.dot(np.dot(X_mean, covariance_inverse), X_mean.transpose()))
        constant = np.sqrt(((2*math.pi)**N) * covariance_determinant)
        return exponential/constant
    
    
    """-------------------------------------------------------------------------
    POSTERIOR STRUCTURE :
        PROBABILITY MATRICES for a cluster probabilities of all points
        
            [(lambda_1)*(P_1), (lambda_1)*(P_2) ........... (lambda_1)*(P_M)]
            [(lambda_2)*(P_1), (lambda_2)*(P_2) ........... (lambda_2)*(P_M)]
            .
            .
            .
            [(lambda_k)*(P_1), (lambda_k)*(P_2) ........... (lambda_k)*(P_M)]
            
        CUMULATIVE PROBABILITY MATRIX is a vertical sum of all these matrices
            ==> Probability sum of all clusters
        
        Performing an element wise Divide Operation for both matrices, gives us
        POSTERIORS :
            [
                    [q_1(1), q_2(1), q_3(1) .........................q_M(1)], 
                    [q_1(2), q_2(2), q_3(2) .........................q_M(2)], 
                    .
                    .
                    .
                    [q_1(k), q_2(k), q_3(k), ...................q_M(k)]                    
            ]
    
    ------------------------------------------------------------------------""" 
    
    def expectation(self, means, covariances, lambdas, X):
        K = self.n_clusters
        M, N = X.shape
        probabilities = np.empty((K, M))
        for k in range(K):
            mean_k = means[k]
            covariance_k = covariances[k]
            lambda_k = lambdas[k]
            for m in range(M):
                X_m = X[m]
                probability = self.guassian(X_m, mean_k, covariance_k)
                probabilities[k][m] = lambda_k*probability        
        cumulative_probabilities = np.sum(probabilities, axis = 0)
        posteriors = probabilities/cumulative_probabilities  
        
        return posteriors
    
    """-------------------------------------------------------------------
        POSTERIORS : (K,M) posteriors of all points corresponding to k clusters
        X : (M,N)
        
        [
            [q_k_1*X_1_1, q_k_1*X_1_2, ......................... q_k_1*X_1_N],
            [q_k_2*X_2_1, q_k_2*X_2_2, ......................... q_k_2*X_2_N],
            .
            .
            .
            [q_k_M*X_M_1, q_k_M*X_M_2, ......................... q_k_M*X_M_N]
        ]
        
        mean of cluster : (posterior of all datapoints from this cluster)*(data point)/(sum of posteriors of all data points)
        
    ---------------------------------------------------------------------"""
    def maximization(self, posteriors, X):
        M, N = X.shape
        K, M = posteriors.shape
        
        means = np.zeros((K, N))
        covariances = np.zeros((K, N, N))
        lambdas = np.zeros(K)
        
        for k in range(K):
            q_k = posteriors[k].reshape(M, 1)
            q_sum_k = np.sum(q_k)
            
            mean_k = (np.sum(q_k*X, axis=0) / q_sum_k).reshape(1, N)
            means[k] = mean_k
            
            covariance_k = np.zeros((N,N))
            for m in range(M):
                X_m_k = (X[m] - mean_k).reshape(1, N)
                covariance_k = covariance_k + q_k[m] * np.outer(X_m_k, X_m_k)
            covariance_k = covariance_k/q_sum_k
            covariance_k = covariance_k + 1e-6*np.identity(N)
            covariances[k] = covariance_k
            
            lambda_k = q_sum_k/M
            lambdas[k] = lambda_k
        
        return means, covariances, lambdas
    
    
    """----------------------------------------------------------------------------------------------
    ASSUMPTION : 
        P(x_m | Y = k, theta) = N(x_m| mean_k, covariance_k)
        P(Y = y | theta) = lambda_k
        
    LOG LIKELIHOOD :
        sum of all points
            log(
                for each cluster
                    sum( lambda_k * N(x_m| mean_k, covariance_k) )
            )               
    
    ------------------------------------------------------------------------------------------------"""
    def compute_log_likelihood(self, means, covariances, lambdas, X):
        M, N = X.shape
        K = self.n_clusters
        log_likelihood = 0        
        for m in range(M):
            X_m_prob = 0
            for k in range(K):
                X_m_prob = X_m_prob + lambdas[k] * self.guassian(X[m], means[k], covariances[k])
            log_likelihood = log_likelihood + np.log(X_m_prob)            
        return log_likelihood
    
    def fit(self, X):
        (means, covariances, lambdas) = self.get_initial_parameters(X)
        previous_loglikelihood = 0
        current_loglikelihood = 1e+10
        iterations = 0
        while abs(current_loglikelihood - previous_loglikelihood) > self.tol:
            print('--------------------------------------------------------------------')
            print('ITERATION ', iterations)

            posteriors = self.expectation(means, covariances, lambdas, X)
            (means, covariances, lambdas) = self.maximization(posteriors, X)

            previous_loglikelihood = current_loglikelihood
            current_loglikelihood = self.compute_log_likelihood(means, covariances, lambdas, X)
            
            print('PREVIOUS LOG LIKELIHOOD ', previous_loglikelihood)
            print('CURRENT LOG LIKELIHOOD ', current_loglikelihood)
            iterations = iterations + 1
            print('--------------------------------------------------------------------')
            
        return (means, covariances, lambdas, current_loglikelihood)

    
M, N = data_train.shape
cluster_centers = data_train[:, 0]
X = data_train[:, 1:N]

k_list = [12, 18, 24, 36, 42]
tol = 1e-4
max_iter = 1e+4

log_likelihood_matrix = np.empty((20, 5))

for i in range(20):
    for j in range(len(k_list)):
        print('#############################################################################')
        k = k_list[j]
        print('RUNNING GMM FOR ', k)
        gmm = GMM(k, tol, max_iter)
        (means, covariances, lambdas, current_loglikelihood) = gmm.fit(X)
        log_likelihood_matrix[i][j] = current_loglikelihood
