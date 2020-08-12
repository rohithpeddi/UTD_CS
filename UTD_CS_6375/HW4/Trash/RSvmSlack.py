# coding:utf-8
import math
import numpy as np
from cvxopt import solvers,matrix
from pdb import set_trace

class SlackSVM:
    def fit(self,X,Y,c):
        assert(Y.shape == (X.shape[0],))
        n_feature = X.shape[1]
        n_sample = Y.size
        n_paras = n_feature + 1 + n_sample
        # construct P
        P = np.zeros(n_paras)
        for i in range(n_feature):
            P[i]=1
        P = np.diag(P)

        # construct q
        q = np.zeros(n_paras)
        for i in range(n_sample):
            q[n_feature+1+i]=c

        # construct G phase 1, consider y(wx+b)>=1-ksi
        G = []
        for i in range(n_sample):
            #form: y_i*x_i,y_i,0..0,1,0..0
            tmp = np.zeros(n_paras)
            x_i = X[i,:]
            y_i = Y[i]
            tmp[0:n_feature] = y_i*x_i
            tmp[n_feature] = y_i
            tmp[n_feature+1+i] = 1
            G.append(tmp)

        # construct G phase 2, consider ksi >= 0
        for i in range(n_sample):
            tmp = np.zeros(n_paras)
            tmp[n_feature+1+i] =1
            G.append(tmp)
        G = np.array(G)

        # construct h
        h=np.zeros(n_sample*2)
        for i in range(n_sample):
            h[i]=1

        # transform Gx >= h to Gx <= h
        G=-G; h=-h

        P = matrix(P)
        q = matrix(q)
        G = matrix(G)
        h = matrix(h)
        ret = solvers.qp(P,q,G,h)
        solution = ret['x']

        # decompose solution to w,b,ksi
        w = solution[0:n_feature]
        w = np.array(w).flatten()
        b = float(solution[n_feature])
        # ksi = list(solution[n_feature+1:])
        # verify(X,Y,w,b,ksi)
        self.W  = w
        self.b = b
        return self

    def predict(self,X):
        assert(X.shape[1] == self.W.size)
        W = self.W.reshape(-1,1)
        t = np.dot(X,W) + self.b
        t = t.flatten()
        t[t>0] = 1
        t[t<0] = -1
        return t

    def evaluate(self,X,Y):
        assert(Y.shape == (X.shape[0],))
        t = self.predict(X)
        n_right = np.sum( t == Y )
        accuracy = float(n_right)/t.size
        return accuracy

def import_data(fname,label_col = -1):
    fh = open(fname,'r')
    content = fh.readlines()
    fh.close()
    X=[];Y=[]
    for line in content:
        values = line.strip().split(',')
        # assume the label are at the last
        Y.append(values[label_col])
        values.pop(label_col)
        X.append(values)
    X = np.array(X,dtype='float')
    Y = np.array(Y,dtype='float')
    # map labels to +- 1
    Y = (Y-0.5)*2
    Y = Y.astype(int)
    return X,Y

# the function that used to verify the results of qp solver
def verify(X,Y,w,b,ksi):
    n_sample = Y.size
    for i in range(n_sample):
        y_i = Y[i]
        x_i = X[i,:]
        val = y_i*(np.sum(w*x_i)+b) + ksi[i]
        if  val < 1:
            print("ERROR FIND :",val)
            exit(0)
    return 0


if __name__ == '__main__':
    X_t,Y_t = import_data('sonar_train.data')
    X_v,Y_v = import_data('sonar_valid.data')
    X_test,Y_test = import_data('sonar_test.data')

    C_list = [1,10,1e+2,1e+3]
    accuracy = {'t':[],'v':[]}

    for c in C_list:
        print('Working on c={}'.format(c))
        clr = SlackSVM().fit(X_t,Y_t,c)
        accuracy['t'].append(clr.evaluate(X_t,Y_t))
        accuracy['v'].append(clr.evaluate(X_v,Y_v))

    tmp = accuracy['v']
    # find best parameter combination
    max_accuracy = max(tmp)
    max_configs = list(filter(lambda x:x[1]==max_accuracy, zip(C_list,tmp) ))

    print("1.1(b) accuracy",accuracy['t'])
    print("1.1(c) accuracy",accuracy['v'])

    for c,acc in max_configs:
        clr = SlackSVM().fit(X_t,Y_t,c)
        print("1.1(c) Best C ",c)
        print("1.1(d) accuracy",clr.evaluate(X_test,Y_test))