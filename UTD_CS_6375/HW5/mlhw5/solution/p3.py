#coding:utf-8
import numpy as np
import multiprocessing

class Normalizer:
    def __init__(self,X):
        M,N = X.shape
        x_mu = np.mean(X,axis=1).reshape(M,1)
        st = np.std(X,axis=1).reshape(M,1)
        self.mu =x_mu
        self.st = st

    def norm(self,X):
        X=X-self.mu
        X=X/self.st
        # self._assert(X)
        return X

    def _assert(self,X):
        M,N=X.shape
        for i in range(M):
            data = X[i,:]
            x_mean = np.mean(data)
            x_std = np.std(data)
            assert(abs(x_mean)<EPS)
            assert(abs(x_std-1)<EPS)
        return

class LogisticRegression:
    def __init__(self,**kwargs):
        if 'regularize' in kwargs:
            assert('L' in kwargs),"missing lambda"
            self.regularize=kwargs['regularize']
            self.L = kwargs['L']
        else:
            self.L=0.0
            self.regularize=None
        if 'maxstep' in kwargs:
            self.stepLimit=kwargs['maxstep']
        else:
            self.stepLimit=5e3

        if 'stepsize' in kwargs:
            self.stepsize=kwargs['stepsize']
        else:
            self.stepsize=lambda x: 1/(1+np.sqrt(x))

    def _penalty(self,w,j):
        if self.regularize == None:
            return 0.0
        if self.regularize == 'L2':
            return self.L * w[j]
        if self.regularize == 'L1':
            return self.L * np.sign(w[j])
        assert(False),"Something Wrong"

    def _P(self,x,W,b):
        exponent = float(np.dot(W.T,x)+b)
        if exponent>100:
            return 0.999995
        else:
            tmp = np.exp(exponent)
            return float(tmp/(1+tmp))

    def fit(self,X,Y):
        # check Y is valid
        labels = np.unique(Y)
        assert(np.sum(labels)==0 and np.max(labels)==1), "Label Error"
        M,N=X.shape
        W = np.ones((M,1))
        b = 0.0
        # lr = 0.1 # learning rate
        step = 1
        while True:
            # calculate the gradient
            grad_b = 0.0
            for i in range(N):
                y_i = Y[0,i]
                x_i = X[:,i:i+1]
                grad_b+= (y_i+1)/2.0-self._P(x_i,W,b)
            grad_W = np.zeros((M,1))
            for j in range(M):
                for i in range(N):
                    y_i = Y[0,i]
                    x_i = X[:,i:i+1]
                    grad_W[j,0]+=((y_i+1)/2.0-self._P(x_i,W,b))*X[j,i]
                grad_W[j] -= self._penalty(W,j)
            # set the new W and b
            W += grad_W * self.stepsize(step)
            b += grad_b * self.stepsize(step)
            step += 1
            # check convergence
            grad_val = max(np.max(abs(grad_W)),abs(grad_b))
            if grad_val < 0.05 or step > self.stepLimit:
                break
            else:
                pass
                # if step%500==0:
                # 	logsum=0.0
                # 	for i in range(N):
                # 		if Y[0,i]>0.5:
                # 			prob = self._P(X[:,i:i+1],W,b)
                # 		else:
                # 			prob = 1-self._P(X[:,i:i+1],W,b)
                # 		logsum+=np.log(prob)
                # 	print step,"\tGradient:",grad_val,"\tLogLike:",logsum

        self.W = W
        self.b = b

    def predict(self,X):
        M,N=X.shape
        assert(M == self.W.size)
        ret = np.dot(self.W.T,X)+self.b
        return ret.reshape((1,N))

    def evaluate(self,X,Y):
        pred = self.predict(X)
        ans = np.multiply(pred,Y)
        N_right =  ans[ans>0].size
        return float(N_right)/Y.size

def import_data(fname):
    fh = open(fname,'r')
    content = fh.readlines()
    fh.close()
    X=[];Y=[]
    for line in content:
        values = line.strip().split(',')
        X.append(values[0:-1])
        Y.append(values[-1])
    X= np.array(X,dtype='float').T
    Y= np.array([Y],dtype='float')
    Y = (Y-1.5)*2
    Y.astype('int')
    return X,Y

def run_exp(args):
    Xtr,Ytr,paraL,preg = args
    logReg=LogisticRegression(L=paraL,regularize=preg)
    logReg.fit(Xtr,Ytr)
    return (logReg.L,logReg.W,logReg.b,logReg.regularize)

def neat_print(dataTuple):
    L,W,b,rgl = dataTuple
    print("==========L:{},reguarize:{}==========".format(L,rgl))
    logReg=LogisticRegression()
    logReg.W= W;logReg.b=b
    print("Train accuracy:", logReg.evaluate(Xtr,Ytr))
    print("Valid accuracy:", logReg.evaluate(Xvd,Yvd))
    print("Test accuracy:", logReg.evaluate(Xts,Yts))
    print("Learned W:", end='')
    w_str= []
    for i in range(logReg.W.size):
        w_str.append('%0.2f' %logReg.W[i,0])
    print(','.join(w_str))
    print('Learned b:',logReg.b)

if __name__ == '__main__':
    Xtr,Ytr = import_data("../sonar_train.data")
    Xvd,Yvd = import_data("../sonar_valid.data")
    Xts,Yts = import_data("../sonar_test.data")
    normer = Normalizer(Xtr)
    Xtr=normer.norm(Xtr)
    Xvd=normer.norm(Xvd)
    Xts=normer.norm(Xts)
    # Q2.1
    ret=run_exp((Xtr,Ytr,0.0,None))
    neat_print(ret)
    # considered lambdas
    pLambda = []
    for i in range(-5,1):
        value =10**i
        pLambda.append(value)
        pLambda.append(5*value)
    # multi process parallel
    pool = multiprocessing.Pool()

    # Q2.2 and Q2.3
    arguments=[]
    for l in pLambda:
        arguments.append( (Xtr,Ytr,l,"L2") )
        arguments.append( (Xtr,Ytr,l,"L1") )
    lrObjs = pool.map(run_exp,arguments)
    pool.close()
    pool.join()
    for lr in lrObjs:
        neat_print(lr)
