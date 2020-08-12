import numpy as np
import pandas as pd
import quadprog as quad

data_train = pd.read_csv("spam_train.data").values
X_train = data_train[:, 0:57]
Y_train = data_train[:, 57]
NUM, DIM = X_train.shape
Y_train = Y_train.reshape(NUM,1)
X_train = np.concatenate((X_train, np.ones((NUM,1))), axis=1)

#data_val = pd.read_csv("spam_validation.data").values
#X_val = data_val[:, 0:57]
#Y_val = data_val[:, 57]
#NUM, DIM = X_val.shape
#Y_val = Y_val.reshape(NUM,1)
#X_val = np.concatenate((X_val, np.ones((NUM,1))), axis=1)
#
#data_test = pd.read_csv("spam_test.data").values
#X_test = data_test[:, 0:57]
#Y_test = data_test[:, 57]
#NUM, DIM = X_test.shape
#Y_test = Y_test.reshape(NUM,1)
#X_test = np.concatenate((X_test, np.ones((NUM,1))), axis=1)

#def train(X,Y,c):       
#    NUM, DIM = X.shape    
#    P = np.concatenate((np.eye(NUM+DIM, M=DIM).T, np.zeros((DIM,NUM+DIM))), axis = 0)
#    q = np.concatenate((np.zeros((DIM,1)),c*np.ones((NUM,1))), axis=0)
#    #P = np.eye(DIM)
#    #q = np.zeros(DIM)
#    
#    G_u = np.concatenate((X_train*Y_train*-1., np.eye(NUM)), axis = 1)
#    G_l = np.concatenate((np.zeros((NUM,DIM)), np.eye(NUM)), axis = 1)
#    
#    G = np.concatenate((G_u, G_l), axis=0)
#    #G = X*Y*-1.
#    #h = np.ones(NUM)*-1. 
#    
#    h = np.concatenate((-1.*np.ones((NUM, 1)), np.zeros((NUM,1))), axis=0)
#    
#    return quad.solve_qp(.5 * P, q, -G.T,  -h, 0)
#
#def validate():
#    return
#
#def test():
#    return
#
#def score(W, X, Y):    
#    pred = np.dot(X, W)
#    pred[pred>0] = 1
#    pred[pred<0] = -1    
#    return np.sum(pred-Y)
#
#def support_vectors(X, lagrange):
#    lagrange = lagrange > 0
#    return X[lagrange.ravel()]

#featureMap = featureTransformation(X)
#solution = train(X_train,Y_train,1)
c = 1
NUM, DIM = X_train.shape    
P = np.concatenate((np.eye(NUM+DIM, M=DIM).T, np.zeros((NUM,NUM+DIM))), axis = 0)
q = -1.*np.concatenate((np.zeros((DIM,1)),c*np.ones((NUM,1))), axis=0)
#P = np.eye(DIM)
#q = np.zeros(DIM)

G_u = np.concatenate((X_train*Y_train, np.eye(NUM)), axis = 1)
G_l = np.concatenate((np.zeros((NUM,DIM)), np.eye(NUM)), axis = 1)

G = np.concatenate((G_u, G_l), axis=0)
#G = X*Y*-1.
#h = np.ones(NUM)*-1. 

h = np.concatenate((np.ones((NUM, 1)), np.zeros((NUM,1))), axis=0)
solution = quad.solve_qp(.5 * P, q, G.T,  h, 0)

W = solution[0]