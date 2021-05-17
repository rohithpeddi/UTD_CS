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
# ----------------- CONJUGATE GRADIENT DESCENT -------------------
###################################################################

def gdConjugate(funObj, w, maxEvals, alpha, gamma, X, y, lambd, verbosity, freq):
    [fkp1, gkp1] = funObj(w, X, y, lambd)
    functionEvaluations = 1
    functionValues = []
    functionValues.append(fkp1)

    totalBacktracks = 0
    dk = -1*gkp1
    fk = fkp1
    gk = gkp1
    # alpha = 1/LA.norm(gk)
    while True:
        wTemp = w + alpha*dk
        [fTemp, gTemp] = funObj(wTemp, X, y, lambd)
        functionEvaluations += 1
        functionValues.append(fTemp)

        if functionEvaluations > 2:
            alpha = min(1, 2 * (fk - fkp1) / np.dot(gkp1.T, gkp1)[0, 0])
            beta = np.dot(gkp1.T, gkp1)[0, 0] / np.dot(gk.T, gk)[0, 0]
            dkp1 = -1*gkp1 + beta * dk
        else:
            dkp1 = -1*gkp1

        dk = dkp1

        backtracks = 0
        while fTemp > fkp1 - gamma*alpha*np.dot(gkp1.T, -1*dk)[0, 0]:
            alpha = alpha * alpha * np.dot(gkp1.T, -1*dk)[0, 0] / (2 * (fTemp + np.dot(gkp1.T, -1*dk)[0, 0] * alpha - fkp1))
            wTemp = w + alpha*dk
            [fTemp, gTemp] = funObj(wTemp, X, y, lambd)
            functionValues.append(fTemp)
            functionEvaluations += 1
            backtracks += 1
            totalBacktracks += 1

        fk = fkp1
        gk = gkp1
        fkp1 = fTemp
        gkp1 = gTemp
        w = wTemp
        optimalityCondition = LA.norm(gkp1, np.inf)
        if (verbosity > 0) and (functionEvaluations % freq == 0):
            print("fEvals: " + str(functionEvaluations) + ", alpha = " + str(alpha) + ", fValue = " + str(fkp1) + ", OptCond: " + str(optimalityCondition))
        if (optimalityCondition < 1e-2) or (functionEvaluations > maxEvals):
            break

    return functionValues

[nSamples, nVars] = X.shape
w = np.zeros((nVars, 1))
print('------------------------------------------------------------------')
print('------------------------LOGISTIC LOSS------------------------------')
print('------------------------------------------------------------------')
print("Gradient Descent with line search")
gdConjugateLFunV1 = gdConjugate(LogisticLossVectorized, w, 250, 1, 1e-4, X, y, 1, 1, 10)

print('------------------------------------------------------------------')
print('------------------------HINGE LOSS------------------------------')
print('------------------------------------------------------------------')
print("Gradient Descent with line search")
gdConjugateHFunV1 = gdConjugate(HingeLossVectorized, w, 250, 1, 1e-4, X, y, 1, 1, 10)


