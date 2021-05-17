from scipy.io import loadmat
import numpy as np
from numpy import linalg as LA

X = loadmat(r"train.mat")
y = np.loadtxt(r"train.targets")

# Statistics of the Dense Format of X
X = X['X'].todense()
print(X.shape)


def LogisticLoss(w, X, y, lambd):
    Xw = np.dot(X, w)
    yt = y.reshape(-1, 1)

    ytXw = np.multiply(yt, Xw)

    f = np.sum(np.logaddexp(0, -ytXw)) + lambd * np.sum(np.abs(w))

    gmul = -1 * np.multiply(yt, 1 / (1 + np.exp(ytXw)))
    g = (np.dot(gmul.reshape(1, -1), X) + lambd * np.sign(w).reshape(1, -1)).reshape(-1,1)

    return [f, g]


[nSamples, nVars] = X.shape
w = np.zeros((nVars, 1))
[f, g] = LogisticLoss(w, X, y, 1)
print(f)
print(g)

###############################################################################
# ------------------------ PROXIMAL GRADIENT DESCENT -------------------------
###############################################################################

def gdFixed(funObj, w, maxEvals, alpha, X, y, lambd, verbosity, freq):
    functionEvaluations = 0
    functionValues = []
    while True:
        [f, g] = funObj(w, X, y, lambd)
        functionEvaluations += 1
        functionValues.append(f)
        w = w - alpha * g
        optimalityCondition = LA.norm(g, np.inf)
        if (verbosity > 0) and (functionEvaluations % freq == 0):
            print(functionEvaluations, alpha, f, optimalityCondition)
        if (optimalityCondition < 1e-2) or (functionEvaluations > maxEvals):
            break
    return functionValues

def computeL1Prox(z, lambd):
    return np.multiply(np.maximum(0, np.abs(z) - lambd), np.sign(z))

def gdProx(funObj, w, maxEvals, alpha, X, y, lambd, verbosity, freq):
    functionEvaluations = 0
    functionValues = []
    while True:
        [f, g] = funObj(w, X, y, 0)
        w = w - alpha * g
        w = computeL1Prox(w, lambd * alpha)
        functionEvaluations += 1
        functionValues.append(f)
        optCond = LA.norm(g, np.inf)
        if (verbosity > 0) and (functionEvaluations % freq == 0):
            print(functionEvaluations, alpha, f, optCond)
        if (optCond < 1e-2) or (functionEvaluations > maxEvals):
            break
    return functionValues


[nSamples, nVars] = X.shape
w = np.zeros((nVars, 1))
print("Gradient Descent with Fixed Step Size")
funV1 = gdFixed(LogisticLoss, w, 200, 1e-5, X, y, 1000, 1, 10)
print(len(funV1))
print("Proximal Gradient Descent")
(funV3) = gdProx(LogisticLoss, w, 200, 1e-5, X, y, 1000, 1, 10)
print(len(funV3))