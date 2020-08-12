#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 22:29:52 2020

@author: rohith
"""

import pandas as pd
from sklearn import svm
from sklearn.metrics import accuracy_score

svmd = pd.read_csv("mystery.data", names=["X1","X2","X3","X4","Y"])
X = svmd.loc[:, "X1":"X4"]
#X['Xb'] = 1
#X = X.values
Y = svmd.loc[:, "Y"]

clf = svm.SVC(kernel='linear')
clf.fit(X, Y)


print(accuracy_score(Y, clf.predict(X)))