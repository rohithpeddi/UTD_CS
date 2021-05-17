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
# -------------- NUMERICALLY STABLE VERSION ------------------------
########################################################

def HingeLossForLoop(w, X, y, lambd):
    # Computes the cost function for all the training samples
    f = 0
    g = 0
    for i in range(len(X)):
        fwp = np.dot(X[i], w)
        f = f + np.max([0, 1 - y[i] * fwp])
        g = g - y[i] * X[i] * np.double(1 > y[i] * fwp)
    f = f + lambd * np.sum(np.multiply(w, w))
    g = g + 2 * lambd * w.reshape(1, -1)
    return [f, g]

start = time.time()
[f, g] = HingeLossForLoop(w, X, y, 1)
end = time.time()
print("Time Taken = " + str(end - start))
print("Function value = " + str(f))
print("Printing Gradient:")
print(g)

###################################################################

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

def HingeLossVectorized(w, X, y, lambd):
    # Computes the cost function for all the training samples
    fwp = np.dot(X, w)
    yt = y.reshape(-1, 1)
    yfwp = np.multiply(yt, fwp)

    f = np.sum(np.maximum(0, 1-yfwp)) + lambd*np.sum(np.multiply(w, w))

    indicator = np.double(1 > yfwp)
    indicator_mul = np.multiply(-yt, indicator)

    g = (np.dot(indicator_mul.reshape(1, -1), X) + lambd* w.reshape(1, -1)).reshape(-1, 1)
    return [f, g]



start = time.time()
[f, g] = HingeLossVectorized(w, X, y, 1)
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
[f1, g1] = HingeLossForLoop(w, X, y, 1)
end = time.time()
print("Time Taken = " + str(end - start))
print("Function value Naive = " + str(f1))
print("Printing Gradient Naive:")
print(g1)

start = time.time()
[f2, g2] = HingeLossVectorized(w, X, y, 1)
end = time.time()
print("Time Taken = " + str(end - start))
print("Function value For = " + str(f2))
print("Printing Gradient For:")
print(g2)


####################################################################
# ------ MAKING SURE GRADIENT IS COMPUTED CORRECTLY ---------------
####################################################################

funObj = lambda wc : HingeLossForLoop(wc, X, y, 1)[0]

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

gn = numericalGrad(funObj, w, 1e-10)
fn = funObj(w)
print(f)
print(fn)
print(gn)
print(g)