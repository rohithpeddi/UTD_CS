from scipy.io import loadmat
import numpy as np
from numpy import linalg as LA

X = loadmat(r"../train.mat")
y = np.loadtxt(r"../train.targets")

# Statistics of the Dense Format of X
X = X['X'].todense()
print(X.shape)

###################################################################
# -------------- LOGISTIC LOSS VECTORIZED VERSION -----------------
####################################################################

def LogisticLossVectorized(w, X, y, lambd):
    fwp = np.dot(X, w)
    yt = y.reshape(-1, 1)
    yfwp = np.multiply(yt, fwp)

    f = np.sum(np.logaddexp(0, -yfwp)) + lambd*np.sum(np.multiply(w, w))
    g1 = 1 / (1 + np.exp(yfwp))
    g2 = (-1 * np.multiply(yt, g1)).reshape(1, -1)
    g = (np.dot(g2, X) +  2 * lambd * w.reshape(1, -1)).reshape(-1, 1)
    return [f, g]

def LogisticLossVectorized2(w, X, y, lam):
    # Computes the cost function for all the training samples
    m = X.shape[0]
    Xw = np.dot(X,w)
    yT = y.reshape(-1,1)
    yXw = np.multiply(yT,Xw)
    f = np.sum(np.logaddexp(0,-yXw)) + 0.5*lam*np.sum(np.multiply(w,w))
    gMul = 1/(1 + np.exp(yXw))
    ymul = -1*np.multiply(yT, gMul)
    g =  np.dot(ymul.reshape(1,-1),X) + lam*w.reshape(1,-1)
    g = g.reshape(-1,1)
    return [f, g]


###################################################################
# -------------- HINGE LOSS VECTORIZED VERSION --------------------
####################################################################

def HingeLossVectorized(w, X, y, lambd):
    fwp = np.dot(X, w)
    yt = y.reshape(-1, 1)
    yfwp = np.multiply(yt, fwp)

    f = np.sum(np.maximum(0, 1-yfwp)) + lambd * np.sum(np.multiply(w, w))

    indicator = np.double(1 > yfwp)
    indicator_mul = np.multiply(-yt, indicator)

    g = (np.dot(indicator_mul.reshape(1, -1), X) + 2*lambd * w.reshape(1, -1)).reshape(-1, 1)
    return [f, g]

###################################################################
# -------------- ACCELERATED GRADIENT DESCENT ------------------
####################################################################


def gdAccelerated(funObj, w, maxEvals, alpha, gamma, X, y, lam, verbosity, freq):
    [f, g] = funObj(w, X, y, lam)
    functionEvaluations = 1
    functionValues = []
    functionValues.append(f)

    lambda_prev = 0
    lambda_curr = 1
    beta = 1
    x = w
    y_prev = x
    alpha = 1/LA.norm(g)
    while True:
        y_curr = x - alpha * g
        x = (1 - beta) * y_curr + beta * y_prev
        y_prev = y_curr

        lambda_tmp = lambda_curr
        lambda_curr = (1 + np.sqrt(1 + 4 * lambda_prev * lambda_prev)) / 2
        lambda_prev = lambda_tmp
        beta = (1 - lambda_prev) / lambda_curr

        [f, g] = funObj(x, X, y, lam)
        functionEvaluations += 1
        functionValues.append(f)
        optCond = LA.norm(g, np.inf)
        if ((verbosity > 0) and (functionEvaluations % freq == 0)):
            print(functionEvaluations, alpha, f, optCond)
        if (optCond < 1e-2) or (functionEvaluations >= maxEvals):
            break
    return functionValues


[nSamples, nVars] = X.shape
w = np.zeros((nVars, 1))
print('------------------------------------------------------------------')
print('------------------------LOGISTIC LOSS------------------------------')
print('------------------------------------------------------------------')
print("Accelerated Gradient Descent with line search")
gdAcceleratedLFunV1 = gdAccelerated(LogisticLossVectorized, w, 250, 1, 1e-4, X, y, 1, 1, 10)


print('------------------------------------------------------------------')
print('------------------------HINGE LOSS------------------------------')
print('------------------------------------------------------------------')
print("Accelerated Gradient Descent with line search")
gdAcceleratedHFunV1 = gdAccelerated(HingeLossVectorized, w, 250, 1, 1e-4, X, y, 1, 1, 10)
