import numpy as np
import pandas as pd
import quadprog as quad

svm = pd.read_csv("mystery.data", names=["X1","X2","X3","X4","Y"])
X = svm.loc[:, "X1":"X4"]
X['Xb'] = 1
X = X.values
Y = svm.loc[:, "Y":].values

## SOLVING PRIMAL PROBLEM USING FEATURE TRANSFORMATION
def featureTransformation(X):
    ft = []    
    
    ftx31 = X[:,0].reshape(1000,1)**3
    ftx32 = X[:,1].reshape(1000,1)**3
    ftx33 = X[:,2].reshape(1000,1)**3
    ftx34 = X[:,3].reshape(1000,1)**3    
    
    ftx21 = X[:,0].reshape(1000,1)**2
    ftx22 = X[:,1].reshape(1000,1)**2
    ftx23 = X[:,2].reshape(1000,1)**2
    ftx24 = X[:,3].reshape(1000,1)**2
    
    
    ftx212 = X[:,0].reshape(1000,1)*X[:,1].reshape(1000,1)
    ftx223 = X[:,1].reshape(1000,1)*X[:,2].reshape(1000,1)
    ftx234 = X[:,2].reshape(1000,1)*X[:,3].reshape(1000,1)
    ftx213 = X[:,0].reshape(1000,1)*X[:,2].reshape(1000,1)
    ftx214 = X[:,0].reshape(1000,1)*X[:,3].reshape(1000,1)
    ftx224 = X[:,1].reshape(1000,1)*X[:,3].reshape(1000,1)
    
    #ft = np.concatenate((ftx31, ftx32, ftx33, ftx34, ftx21, ftx22, ftx23, ftx24, ftx212, ftx223, ftx234, ftx213, ftx214, ftx224, X), axis=1)
    ft = np.concatenate((ftx31, ftx32, ftx33, ftx34, ftx21, ftx22, ftx23, ftx24, ftx212, ftx223, ftx234, X), axis=1)
    #ft = np.concatenate((ftx21, ftx22, ftx23, ftx24, ftx212, ftx223, ftx234, ftx213, ftx214, ftx224, X), axis=1)
    return ft

def solve(X,Y):        
    NUM, DIM = X.shape    
    P = np.eye(DIM)
    q = np.zeros(DIM)
    
    G = featureMap*Y*-1.
    h = np.ones(NUM)*-1. 
    
    return quad.solve_qp(.5 * P, q, -G.T,  -h, 0)

def score(W, X, Y):    
    pred = np.dot(X, W)
    pred[pred>0] = 1
    pred[pred<0] = -1    
    return np.sum(pred-Y)

def support_vectors(lagrange):
    lagrange = lagrange > 0
    return X[lagrange.ravel()]

featureMap = featureTransformation(X)
solution = solve(featureMap,Y)
W = solution[0]

#print("WEIGHT VECTORS ", W[:14]) 
#print("BIAS ", W[14])
#print("MARGIN ",  (1 / np.sqrt((W[0:14] ** 2).sum()))) 
#print("SCORE ", score(W, featureMap, Y))
#print("SUPPORT VECTORS ", support_vectors(solution[4].reshape(1000,1)))

#print("WEIGHT VECTORS ", W[:18]) 
#print("BIAS ", W[18])
#print("MARGIN ",  (1 / np.sqrt((W[0:18] ** 2).sum()))) 
#print("SCORE ", score(W, featureMap, Y))
#print("SUPPORT VECTORS ", support_vectors(solution[4].reshape(1000,1)))

print("WEIGHT VECTORS ", W[:15]) 
print("BIAS ", W[15])
print("MARGIN ",  (1 / np.sqrt((W[0:15] ** 2).sum()))) 
print("ERROR ", score(W.reshape(16,1), featureMap, Y))
print("SUPPORT VECTORS ", support_vectors(solution[4].reshape(1000,1)))
