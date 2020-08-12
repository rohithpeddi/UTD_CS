# -*- coding: utf-8 -*-
"""
Created on Sun May 10 15:58:12 2020

@author: ROHITH PEDDI
"""


import pandas as pd
import numpy as np

R = np.array([
    [0.0, 1.0, 0.5, 0.5],
    [0.5, 0.0, 1.0, 0.5],
    [-1.0, 0.5, 0, 0.5],
    [-1.0, 0.5, 0.5, 0],
    ])

def optimal_values(tol, gamma):
    Values_residual = []
    previous_values = np.zeros(4)
    current_values = np.zeros(4)
    isConvergence = False
    iterations = 0
    while not isConvergence:
        for i in range(4):
            V_i_list = np.zeros(4)
            for j in range(4):
                V_i = R[i][j] + gamma*previous_values[j]
                #print(V_i, R[i][j], gamma, previous_values[j])
                V_i_list[j] = V_i
            max_V_i = np.max(V_i_list)
            current_values[i] = max_V_i
            print(V_i_list)
        
        if np.all(abs(previous_values - current_values) < tol):
            isConvergence = True
        else:
            previous_values = np.copy(current_values)
            Values_residual.append(current_values)
        iterations = iterations + 1
        print('-----------------------------------------------------------')
        print('ITERATION ', iterations)
        print('CURRENT VALUES ', current_values)
    return current_values, Values_residual

(opt_V, V_list)= optimal_values(1e-10, 0.01)