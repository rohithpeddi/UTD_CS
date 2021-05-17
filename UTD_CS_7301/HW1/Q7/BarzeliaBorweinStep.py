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

def LogisticLossVectorized2(w, X, y, lambd):
    fwp = np.dot(X, w)
    yt = y.reshape(-1, 1)
    yfwp = np.multiply(yt, fwp)

    f = np.sum(np.logaddexp(0, -yfwp)) + 0.5*lambd*np.sum(np.multiply(w, w))
    g1 = 1 / (1 + np.exp(yfwp))
    g2 = (-1 * np.multiply(yt, g1)).reshape(1, -1)
    g = (np.dot(g2, X) +  lambd * w.reshape(1, -1)).reshape(-1, 1)
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
# ----------------- BARZELIA BORWEIN GRADIENT DESCENT -------------
###################################################################

def gdBarzelia(funObj, wInit, maxEvals, alpha, gamma, X, y, lambd, verbosity, freq):
    [fk, gk] = funObj(wInit, X, y, lambd)
    functionEvaluations = 1
    functionValues = []
    functionValues.append(fk)

    totalBacktracks = 0
    fkm1 = fk
    gkm1 = gk
    wkm1 = wInit
    while True:
        wTemp = wkm1 - alpha*gk
        [fTemp, gTemp] = funObj(wTemp, X, y, lambd)
        functionValues.append(fTemp)
        functionEvaluations += 1

        if functionEvaluations > 2:
            ykm1 = gk - gkm1
            skm1 = -alpha * gkm1
            alpha = np.dot(skm1.T, ykm1)[0, 0]/np.dot(ykm1.T, ykm1)[0, 0]

        backtracks = 0
        while fTemp > fk - gamma*alpha*np.dot(gk.T, gk):
            alpha = alpha * alpha * np.dot(gk.T, gk)[0, 0] / (2 * (fTemp + np.dot(gk.T, gk)[0, 0] * alpha - fk))
            wTemp = wkm1 - alpha*gk
            [fTemp, gTemp] = funObj(wTemp, X, y, lambd)
            functionEvaluations += 1
            functionValues.append(fk)
            backtracks += 1
            totalBacktracks += 1

        fkm1 = fk
        gkm1 = gk
        wkm1 = wTemp
        fk = fTemp
        gk = gTemp
        optimalityCondition = LA.norm(gk, np.inf)
        if (verbosity > 0) and (functionEvaluations % freq == 0):
            print("fEvals: " + str(functionEvaluations) + ", alpha = " + str(alpha) + ", fValue = " + str(fk) + ", OptCond: " + str(optimalityCondition))
        if (optimalityCondition < 1e-2) or (functionEvaluations > maxEvals):
            break

    return functionValues

[nSamples, nVars] = X.shape
w = np.zeros((nVars, 1))
print('------------------------------------------------------------------')
print('------------------------LOGISTIC LOSS------------------------------')
print('------------------------------------------------------------------')
print("Gradient Descent with line search")
gdBarzeliaLFunV1 = gdBarzelia(LogisticLossVectorized2, w, 250, 1, 1e-4, X, y, 1, 1, 10)


print('------------------------------------------------------------------')
print('------------------------HINGE LOSS------------------------------')
print('------------------------------------------------------------------')
print("Gradient Descent with line search")
gdBarzeliaHFunV1 = gdBarzelia(HingeLossVectorized, w, 250, 1, 1e-4, X, y, 1, 1, 10)