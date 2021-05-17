import numpy as np
import time

########################################################
# -------------- GENERATE DATA ------------------------
########################################################

# Number of instances
n = 100
# Number of Features
m = 10

X = np.random.rand(n, m)
y = np.random.rand(n)

ybin = [(int(yi >= 0.5) - int(yi < 0.5)) for yi in y]
y = np.array(ybin)
w = np.random.rand(m, 1)
print(y)
print(X)


########################################################
# -------------- FOR LOOP BASED ------------------------
########################################################

def LogisticLossForLoop(w, X, y, lambd):
    # Computes the cost function for all the training samples
    f = 0
    g = 0
    for i in range(len(X)):
        fwp = np.dot(X[i], w)
        f = f + np.log(1 + np.exp(-y[i]*fwp))
        g = g + -y[i]/(1 + np.exp(y[i]*fwp))*X[i]
    f = f + lambd * np.sum(np.multiply(w, w))
    g = g + 2 * lambd * w.reshape(1, -1)
    return [f, g]

start = time.time()
[f, g] = LogisticLossForLoop(w, X, y, 1)
end = time.time()
print("Time Taken = " + str(end - start))
print("Function value = " + str(f))
print("Printing Gradient:")
print(g)

###################################################################
# -------------- NUMERICALLY STABLE VERSION ------------------------
####################################################################

def LogisticLossForLoopStable(w, X, y, lambd):
    # Computes the cost function for all the training samples
    m = X.shape[0]
    f = 0
    g = 0
    for i in range(len(X)):
        fwp = np.dot(X[i], w)
        f = f + np.logaddexp(0, -y[i]*fwp)
        g = g + -y[i]/(1 + np.exp(y[i]*fwp))*X[i]
    f = f + lambd * np.sum(np.multiply(w, w))
    g = g + 2 * lambd * w.reshape(1, -1)
    return [f, g]


start = time.time()
[f, g] = LogisticLossForLoopStable(w, X, y, 1)
end = time.time()
print("Time Taken = " + str(end - start))
print("Function value = " + str(f))
print("Printing Gradient:")
print(g)

###################################################################
# -------------- VECTORIZED VERSION ------------------------
####################################################################

def LogisticLossVectorized(w, X, y, lambd):
    fwp = np.dot(X, w)
    yt = y.reshape(-1, 1)
    yfwp = np.multiply(yt, fwp)

    f = np.sum(np.logaddexp(0, -yfwp)) + lambd*np.sum(np.multiply(w, w))
    g1 = 1 / (1 + np.exp(yfwp))
    g2 = (-1 * np.multiply(yt, g1)).reshape(1, -1)
    g = (np.dot(g2, X) + 2 * lambd * w.reshape(1, -1)).reshape(-1, 1)
    return [f, g]


start = time.time()
[f, g] = LogisticLossVectorized(w, X, y, 1)
end = time.time()
print("Time Taken = " + str(end - start))
print("Function value = " + str(f))
print("Printing Gradient:")
print(g)

###################################################################
# -------------- MAKING SURE BOTH ARE SAME ------------------------
####################################################################

import numpy as np
n = 100
m = 10

X = np.random.rand(n, m)
y = np.random.rand(n)
ybin = [(int(yi >= 0.5) - int(yi < 0.5)) for yi in y]
y = np.array(ybin)
w = np.random.rand(m, 1)

start = time.time()
[f1, g1] = LogisticLossForLoop(w, X, y, 1)
end = time.time()
print("Time Taken = " + str(end - start))
print("Function value Naive = " + str(f1))
print("Printing Gradient Naive:")
print(g1)

start = time.time()
[f2, g2] = LogisticLossVectorized(w, X, y, 1)
end = time.time()
print("Time Taken = " + str(end - start))
print("Function value For = " + str(f2))
print("Printing Gradient For:")
print(g2)


####################################################################
# ------ MAKING SURE GRADIENT IS COMPUTED CORRECTLY ---------------
####################################################################

funObj = lambda wc : LogisticLossForLoop(wc, X, y, 1)[0]

def numericalGrad(funObj, w, epsilon):
        m = len(w)
        grad = np.zeros(m)
        for i in range(m):
            wp = np.copy(w)
            wn = np.copy(w)
            wp[i] = w[i] + epsilon
            wn[i] = w[i] - epsilon
            grad[i] = (funObj(wp) - funObj(wn))/(2*epsilon)
        return grad