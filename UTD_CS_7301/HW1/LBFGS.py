from scipy.io import loadmat
import numpy as np
from numpy import linalg as LA

X = loadmat(r"train.mat")
targets = np.loadtxt(r"train.targets")

# Statistics of the Dense Format of X
X = X['X'].todense()
print(X.shape)

###################################################################
# -------------- LOGISTIC LOSS VECTORIZED VERSION -----------------
####################################################################

def LogisticLossVectorized(w, X, targets, lambd):
    fwp = np.dot(X, w)
    yt = targets.reshape(-1, 1)
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

def HingeLossVectorized(w, X, targets, lambd):
    fwp = np.dot(X, w)
    yt = targets.reshape(-1, 1)
    yfwp = np.multiply(yt, fwp)

    f = np.sum(np.maximum(0, 1-yfwp)) + lambd * np.sum(np.multiply(w, w))

    indicator = np.double(1 > yfwp)
    indicator_mul = np.multiply(-yt, indicator)

    g = (np.dot(indicator_mul.reshape(1, -1), X) + 2*lambd * w.reshape(1, -1)).reshape(-1, 1)
    return [f, g]

###################################################################
# -------------------------- LBFGS --------------------------------
####################################################################

def performLineSearch(funObj, w, X, targets, lambd, functionEvaluations, functionValues, gamma, alpha, f, g, verbosity, freq, maxEvals):
    wTemp = w - alpha * g
    # print(wTemp)
    [fTemp, gTemp] = funObj(wTemp, X, targets, lambd)
    # print("FTemp...." + str(fTemp) + ", gTemp ... " + str(gTemp))
    functionEvaluations += 1
    functionValues.append(f)
    currentBackTracks = 0
    # print(fTemp, f - gamma * alpha * np.dot(g.T, g))
    # print("Alpha : " + str(alpha))
    while fTemp > f - gamma * alpha * np.dot(g.T, g):
        alpha = alpha * alpha * np.dot(g.T, g)[0, 0] / (2 * (fTemp + np.dot(g.T, g)[0, 0] * alpha - f))
        # print("In while block : " + str(alpha))
        wTemp = w - alpha * g
        [fTemp, gTemp] = funObj(wTemp, X, targets, lambd)
        functionEvaluations += 1
        functionValues.append(f)
        currentBackTracks += 1
    w = wTemp
    f = fTemp
    g = gTemp
    optimalityCondition = LA.norm(g, np.inf)
    if (verbosity > 0) and (functionEvaluations % freq == 0):
        print("fEvals: " + str(functionEvaluations) + ", alpha = " + str(alpha) + ", fValue = " + str(
            f) + ", OptCond: " + str(optimalityCondition))
    if (optimalityCondition < 1e-2) or (functionEvaluations > maxEvals):
        # print("Reached optimality or maxEvals")
        return f, g, alpha, w, functionEvaluations, functionValues

    return f, g, alpha, w, functionEvaluations, functionValues

class IterationData:

    def __init__(self, alpha, s, y, ys):
        self.alpha = alpha
        self.s = s
        self.y = y
        self.ys = ys

def gdLBFGS(funObj, w, maxEvals, step, gamma, X, targets, lambd, verbosity, freq, l, epsilon):
    [f, g] = funObj(w, X, targets, lambd)
    step = 1 / LA.norm(g)
    print("Initial Step ... " + str(step))
    functionEvaluations = 1
    functionValues = []
    functionValues.append(f)
    x = w

    # Maintain the list of vectors
    (nX, nY) = w.shape
    vectorList = []
    for i in range(l):
        s = np.zeros(nX)
        y = np.zeros(nY)
        vectorList.append(IterationData(0.0, s, y, 0.0))

    # Compute xnorm and gnorm
    xnorm = max(1, np.sqrt(np.dot(x.T, x)))
    gnorm = np.sqrt(np.dot(g.T, g))

    if gnorm/xnorm <= epsilon:
        print("Found the minimum value")
        return

    descentDirection = -g
    k = 1
    end = 0
    while True:
        fp = f.copy()
        xp = x.copy()
        gp = g.copy()

        # print("Step before line search ... " + str(step))
        [f, g, step, x, functionEvaluations, functionValues] = performLineSearch(funObj, x, X, targets, lambd, functionEvaluations, functionValues, gamma, step, f, g, verbosity, freq, maxEvals)
        # print("Step after line search ... " + str(step))

        xnorm = max(1, np.sqrt(np.dot(x.T, x)))
        gnorm = np.sqrt(np.dot(g.T, g))

        if gnorm / xnorm <= epsilon:
            print("Found the minimum value")
            return

        # Update vectors s and y
        cit = vectorList[end]
        cit.s = x - xp
        cit.y = g - gp

        # Compute scalars ys and yy
        ys = np.dot(cit.y.T, cit.s)
        yy = np.dot(cit.y.T, cit.y)
        cit.ys = ys

        # Computing direction and updating matrices with limited storage
        bound = (l <= k and [l] or [k])[0]
        k = k + 1
        end = (end + 1) % l

        descentDirection = -g
        j = end
        # from later to former
        for i in range(bound):
            j = (j + l - 1) % l
            cit = vectorList[j]
            cit.alpha = np.dot(cit.s.T, descentDirection) / cit.ys
            descentDirection = descentDirection + (cit.y * (-cit.alpha))

        descentDirection = descentDirection * (ys / yy)

        # from former to later
        for i in range(bound):
            cit = vectorList[j]
            beta = np.dot(cit.y.T, descentDirection)
            beta = beta / cit.ys
            descentDirection = descentDirection + (cit.s * (cit.alpha - beta))
            j = (j + 1) % l

        if functionEvaluations > 2:
            step = min(1, 2 * (fp - f) / np.dot(g.T, g)[0, 0])

        optimalityCondition = LA.norm(g, np.inf)
        if (optimalityCondition < 1e-2) or (functionEvaluations > maxEvals):
            print("Reached optimality or maxEvals")
            break

    return functionValues

[nSamples, nVars] = X.shape
w = np.zeros((nVars, 1))
print('------------------------------------------------------------------')
print('------------------------LOGISTIC LOSS------------------------------')
print('------------------------------------------------------------------')
print("Gradient Descent with line search")
gdLBFGSLFunV1 = gdLBFGS(funObj=LogisticLossVectorized, w = w, maxEvals = 250,
                step=1, gamma=1e-4, X=X, targets=targets, lambd=1, verbosity=1, freq=10, l=30, epsilon=1e-5)


print('------------------------------------------------------------------')
print('------------------------HINGE LOSS------------------------------')
print('------------------------------------------------------------------')
print("Gradient Descent with line search")
gdLBFGSHFunV2 = gdLBFGS(funObj=HingeLossVectorized, w = w, maxEvals = 250,
                step=1, gamma=1e-4, X=X, targets=targets, lambd=1, verbosity=1, freq=10, l=30, epsilon=1e-5)



