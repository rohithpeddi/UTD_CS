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
# -------------- GRADIENT DESCENT FIXED LEARNING RATE --------------
####################################################################

def gdFixed(funObj, w, maxEvals, alpha, X, y, lambd, verbosity, freq):
    [f, g] = funObj(w, X, y, lambd)
    functionEvaluations = 1
    functionValues = []
    while True:
        [f, g] = funObj(w, X, y, lambd)
        optimalityCondition = LA.norm(g, np.inf)
        if (verbosity > 0) and (functionEvaluations % freq == 0):
            print(functionEvaluations, alpha, f, optimalityCondition)
        w = w - alpha*g
        functionEvaluations += 1
        if (optimalityCondition < 1e-2) or (functionEvaluations > maxEvals):
            break
        functionValues.append(f)
    return functionValues

[nSamples, nVars] = X.shape
w = np.zeros((nVars, 1))
print('------------------------------------------------------------------')
print('------------------------LOGISTIC LOSS------------------------------')
print('------------------------------------------------------------------')
print("Gradient Descent with Fixed Step Size")
# funV1 = gdFixed(LogisticLossVectorized, w, 250, 1e-5, X, y, 1, 1, 10)
# print(len(funV1))

print('------------------------------------------------------------------')
print('------------------------HINGE LOSS------------------------------')
print('------------------------------------------------------------------')
print("Gradient Descent with Fixed Step Size")
# funV1 = gdFixed(HingeLossVectorized, w, 250, 1e-5, X, y, 1, 1, 10)
# print(len(funV1))

###################################################################
# -------------- GRADIENT DESCENT WITH ARMIJO LINE SEARCH ----------
####################################################################

def gdArmijoV4(funObj, w, maxEvals, alpha, gamma, X, y, lambd, verbosity, freq):
    [f, g] = funObj(w, X, y, lambd)
    alpha = 1/LA.norm(g)
    print("Initial alpha .. " + str(alpha))
    functionEvaluations = 1
    functionValues = []
    functionValues.append(f)
    totalBackTracks = 0
    fOld = f
    gOld = g
    while True:
        wTemp = w - alpha*g
        # print(wTemp)
        [fTemp, gTemp] = funObj(wTemp, X, y, lambd)
        print("FTemp...." + str(fTemp) + ", gTemp ... " + str(gTemp))
        functionEvaluations += 1
        functionValues.append(f)
        currentBackTracks = 0
        # print(fTemp, f - gamma * alpha * np.dot(g.T, g))
        # print("Alpha : " + str(alpha))
        while fTemp > f - gamma*alpha*np.dot(g.T, g):
            alpha = alpha*alpha*np.dot(g.T, g)[0,0]/(2*(fTemp + np.dot(g.T, g)[0,0]*alpha - f))
            print("In while block : " + str(alpha))
            wTemp = w - alpha*g
            [fTemp, gTemp] = funObj(wTemp, X, y, lambd)
            functionEvaluations += 1
            functionValues.append(f)
            currentBackTracks += 1
            totalBackTracks += 1
        fOld = f
        gOld = g
        w = wTemp
        f = fTemp
        g = gTemp
        optimalityCondition = LA.norm(g, np.inf)
        if (verbosity > 0) and (functionEvaluations % freq == 0):
            print("fEvals: " + str(functionEvaluations) + ", alpha = " + str(alpha) + ", fValue = " + str(f) + ", OptCond: " + str(optimalityCondition))
        if (optimalityCondition < 1e-2) or (functionEvaluations > maxEvals):
            break
        if functionEvaluations > 2:
            alpha = min(1, 2*(fOld - f)/np.dot(g.T, g)[0,0])
    return (functionValues, totalBackTracks)


[nSamples, nVars] = X.shape
w = np.zeros((nVars, 1))
print('------------------------------------------------------------------')
print('------------------------LOGISTIC LOSS------------------------------')
print('------------------------------------------------------------------')
print("Gradient Descent with line search")
funV1 = gdArmijoV4(LogisticLossVectorized, w, 250, 1, 1e-4, X, y, 1, 1, 10)
print(len(funV1))

print('------------------------------------------------------------------')
print('------------------------HINGE LOSS------------------------------')
print('------------------------------------------------------------------')
print("Gradient Descent with line search")
# funV2 = gdArmijoV4(HingeLossVectorized, w, 250, 1, 1e-4, X, y, 1, 1, 10)
# print(len(funV2))

