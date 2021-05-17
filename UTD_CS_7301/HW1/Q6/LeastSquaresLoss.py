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
wgen = np.random.rand(m)
y = np.dot(X, wgen) + np.random.normal(0, 0.1, n)
w = np.random.rand(m)
print(y)
print(X)


########################################################
# -------------- FOR LOOP BASED ------------------------
# -------------- NUMERICALLY STABLE VERSION ------------------------
########################################################

def LeastSquaresLossForLoop(w, X, y, lambd):
    f = 0
    g = 0
    for i in range(len(X)):
        fwp = np.dot(X[i], w)
        f = f + np.power(fwp - y[i], 2)
        g = g + 2 * (fwp - y[i]) * X[i]
    f = f + lambd * np.sum(np.multiply(w, w))
    g = g + 2 * lambd * w.reshape(1, -1)
    return [f, g]

start = time.time()
[f, g] = LeastSquaresLossForLoop(w, X, y, 1)
end = time.time()
print("Time Taken = " + str(end - start))
print("Function value = " + str(f))
print("Printing Gradient:")
print(g)

###################################################################
# -------------- VECTORIZED VERSION ------------------------
####################################################################

def LeastSquaresLossVectorized(w, X, y, lambd):
    # Computes the cost function for all the training samples

    Xw = np.matmul(X, w)
    Xwy = (y - Xw).reshape(-1, 1)
    f = np.dot(Xwy.T, Xwy) + lambd * np.sum(w * w)

    fwp = np.dot(X, w).reshape(-1, 1)
    yt = y.reshape(-1, 1)

    f = np.dot((yt-fwp).T, (yt-fwp)) + lambd*np.sum(np.multiply(w,w))
    g = (np.dot((yt-fwp).T, X) + 2*lambd*w.reshape(1, -1)).reshape(1, -1)
    return [f, g]


start = time.time()
[f, g] = LeastSquaresLossVectorized(w, X, y, 1)
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
[f1, g1] = LeastSquaresLossForLoop(w, X, y, 1)
end = time.time()
print("Time Taken = " + str(end - start))
print("Function value Naive = " + str(f1))
print("Printing Gradient Naive:")
print(g1)

start = time.time()
[f2, g2] = LeastSquaresLossVectorized(w, X, y, 1)
end = time.time()
print("Time Taken = " + str(end - start))
print("Function value For = " + str(f2))
print("Printing Gradient For:")
print(g2)


####################################################################
# ------ MAKING SURE GRADIENT IS COMPUTED CORRECTLY ---------------
####################################################################

funObj = lambda wc : LeastSquaresLossForLoop(wc, X, y, 1)[0]

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