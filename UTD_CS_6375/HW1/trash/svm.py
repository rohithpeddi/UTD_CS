import numpy as np
import pandas as pd
from cvxopt import matrix as matrix
from cvxopt import solvers as solvers

svm = pd.read_csv("mystery.data", names=["X1","X2","X3","X4","Y"])
X = svm.loc[:, "X1":"X4"]
X['Xb'] = 1
X = X.values
Y = svm.loc[:, "Y":].values

def getDual(X,Y):
    N = len(X)
    dim = 5
    
    P = matrix(.5*np.eye(dim))
    q = matrix(np.zeros(dim))
    
    G = matrix((-1.*Y)*X) 
    h = matrix(-1.*np.ones(N))
        
    return P,q,G,h
        
P,q,G,h = getDual(X,Y)

solvers.options['show_progress'] = True
solvers.options['abstol'] = 1e-10
solvers.options['reltol'] = 1e-10
solvers.options['feastol'] = 1e-10
                
# Train the model (i.e. compute the alphas)
sol = solvers.qp(P,q,G,h)
alpha = np.array(sol['x']).flatten()

w_dual = np.dot(X.T,Y*alpha)

SV = (alpha>1e-6)
#uSV = SV*(alpha<1e-6)
#b_dual = 1.0/(sum(uSV)+10^-10)*(Y[uSV]-np.dot(np.dot(X[uSV,:],X.T),alpha*Y)).sum()

#print alpha.shape
#print w_dual.shape, b_dual
