import numpy as np
import time
import heapq

# Number of instances
n = 100
# Dimensionality of the data
m = 2

V = np.random.rand(n, m)
# print(V)


def _compute_similarity_matrix_(V):
    n, m = V.shape
    S = np.empty((n, n))
    for i in range(n):
        for j in range(n):
            S[i][j] = S[j][i] = -np.dot((V[i] - V[j]).T, (V[i] - V[j]))
    S = np.exp(S)
    return S

class FacilityLocation:

    def __init__(self, V):
        self.V = V
        self.Gn, self.Gm = self.V.shape
        self.S = _compute_similarity_matrix_(self.V)

    # X contains indices of a subset of rows of ground set V.
    def _evaluate_function_(self, X):
        funcValue = 0
        for i in range(self.Gn):
            maxTillNow = 0
            for j in range(len(X)):
                sij = self.S[i][X[j]]
                maxTillNow = max(maxTillNow, sij)
            funcValue += maxTillNow
        return funcValue

    def _evaluate_gain_(self, X, i):
        fX = self._evaluate_function_(X)
        fXi = fX
        if i not in X:
            X.append(i)
            fXi = self._evaluate_function_(X)
            X.remove(i)
        gain = fXi - fX
        # print(fXi, fX)
        return gain


# Making sure the function is monotonic

FL = FacilityLocation(V)

VList = [*range(n)]
# Sampling two subsets from the ground set
kY = 20
Y = list(np.random.choice(VList, kY, replace=False))
# Y = V[randomRowsY, :]

kX = 10
X = list(np.random.choice(Y, kX, replace=False))
# X = Y[randomRowsX, :]

# Ensuring the property of monotonicity
fX = FL._evaluate_function_(X)
fY = FL._evaluate_function_(Y)
print(fX, fY)

# Making sure the function is submodular

# Picking the index of random element not in Y
ri = 0
while True:
    id = int(np.random.rand()*n)
    if id in Y:
        continue
    ri = id
    break

# ri = X[0]

print(Y)
print(X)
print(ri)

# Ensuring the property of submodularity

gYi = FL._evaluate_gain_(Y, ri)
gXi = FL._evaluate_gain_(X, ri)

print(gXi, gYi)

print('------------------------------------------------')
print('-----------------NAIVE GREEDY---------------')
print('------------------------------------------------')

##################################################################
# -------------------- NAIVE GREEDY ALGORITHMS -------------------
##################################################################


def NaiveGreedy(funcObj, k):
    funcEvals = 0
    optimalk = []
    for i in range(k):
        maxGainTillNow = None
        maxGainIndex = None
        gainValue = None
        gainList = []
        for j in range(n):
            if j in optimalk:
                continue
            else:
                gainValue = funcObj._evaluate_gain_(optimalk, j)
                funcEvals += 1
                if maxGainTillNow is None:
                    maxGainTillNow = gainValue
                    maxGainIndex = j
                elif gainValue > maxGainTillNow:
                    maxGainTillNow = gainValue
                    maxGainIndex = j
                gainList.append((gainValue, maxGainIndex))

        optimalk.append(maxGainIndex)

    print("Total gain function evaluations : " + str(funcEvals))
    return optimalk


start = time.time()
optimal = NaiveGreedy(FL, 10)
end = time.time()
print(optimal)
print("Time Taken = " + str(end - start))

print('------------------------------------------------')
print('-----------------LAZY GREEDY---------------')
print('------------------------------------------------')

##################################################################
# -------------------- LAZY GREEDY ALGORITHMS --------------------
##################################################################

def LazyGreedy(funcObj, k):

    funcEvals = 0

    optimalk = []

    # Initialization
    pq = []
    for i in range(n):
        pq.append((-funcObj._evaluate_gain_(optimalk, i), i))
        funcEvals += 1
    heapq.heapify(pq)

    # print(list(pq))

    (gainMax, maxIndex) = heapq.heappop(pq)
    optimalk.append(maxIndex)

    while len(optimalk) < k:

        (staleGain1, maxIndex) = heapq.heappop(pq)
        gainValue = funcObj._evaluate_gain_(optimalk, maxIndex)
        funcEvals += 1

        (staleGain2, secMaxIndex) = heapq.heappop(pq)
        # print(k, gainValue, -fStale2)

        if gainValue > -staleGain2:
            optimalk.append(maxIndex)
            heapq.heappush(pq, (staleGain2, secMaxIndex))
            continue
        else:
            heapq.heappush(pq, (-gainValue, maxIndex))
            heapq.heappush(pq, (staleGain2, secMaxIndex))

            # pq = []
            # for j in range(n):
            #     if j in optimalk:
            #         continue
            #     else:
            #         pq.append((-funcObj._evaluate_gain_(optimalk, j), j))
            #         funcEvals += 1
            # heapq.heapify(pq)
            # print(list(pq))

    print("Total gain function evaluations : " + str(funcEvals))
    return optimalk


start = time.time()
optimal = LazyGreedy(FL, 10)
end = time.time()
print(optimal)
print("Time Taken = " + str(end - start))
