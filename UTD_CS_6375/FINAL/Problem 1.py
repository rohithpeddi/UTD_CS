

# -*- coding: utf-8 -*-
"""
Created on Thu May  7 23:44:45 2020

@author: ROHITH PEDDI
"""

import pandas as pd
import numpy as np
import scipy.linalg as sp

A = np.array([[1.0,2.0],[2.0,-1.0]])
B = np.array([[1,2],[2,4]])

iterations = 0
while iterations<1000:
    psd = A
    cov_A = np.dot(A.transpose(), A)
    print(cov_A)
    sq_A = sp.sqrtm(cov_A)
    print(sq_A)
    psd = 0.5*(psd + sq_A)
    print(psd)
    A[1][1] = psd[1][1]
    print(A)
    iterations = iterations + 1
    print('-------------------------------------------------')
    print('ITERATION ' + str(iterations))