import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data =pd.read_csv("perceptron.data", names=["X1","X2","X3","X4","Y"])

X = data.loc[:, "X1":"X4"]
Y = data.loc[:, "Y":]
X['Xb'] = 1

step_size = 1
loss = 100
misclassifications = []
missclassification_rate = 1000
W = np.array([0,0,0,0,0]).reshape(1,5)
G = np.array([1,1,1,1,1]).reshape(1,5)
W_list = []
G_list = []
loss_list = []
missclassification_list = []

X = X.values
Y = Y.values

def StandardGradientDescent(step_size, precision):
    global G, W
    iterations = 0
    while abs(G).any() > precision :
        Con = (np.dot(X,W.transpose()))*(-1*Y)        
        Con[Con>=0] = 1
        Con[Con<0] = 0
        G = np.sum((Con*Y)*X, axis=0)
        W = W + step_size*(G)
        W_list.append(W.tolist())
        iterations = iterations+1    
    return iterations

#print("ITERATIONS ", StandardGradientDescent(1,0.01))
#print("WEIGHTS AND BIASES (THE LAST TERM IN EACH LIST) FOR FIRST THREE ITERATIONS ", W_list[0:3])
#print("FINAL WEIGHT AND BIAS : ", W)


iterations = 0
index = 0
def StochasticGradientDescent(step_size, precision):
    global G, W, loss, missclassification_rate, index, iterations    
    pred = []
    while missclassification_rate > 0 :        
        pred = np.dot(X, W.transpose())
        pred[pred>0] = 1
        pred[pred<0] = -1
        misclassifications = abs(pred - Y)
        missclassification_rate = np.sum(misclassifications)
        missclassification_list.append(missclassification_rate)
        
        if misclassifications[index%1000] == 0:
            while misclassifications[index%1000] == 0:
                index = index+1
                
        G = (Y[index%1000]*X[index%1000])
        
        iterations = iterations+1
        index = index+1
        
        W = W + step_size*(G)
        W_list.append(W.tolist())
        
    return iterations

print("ITERATIONS ", StochasticGradientDescent(1,0))
print("WEIGHTS AND BIASES (THE LAST TERM IN EACH LIST) FOR FIRST THREE ITERATIONS ", W_list[0:3])
print("FINAL WEIGHT AND BIAS : ", W)
plt.plot(missclassification_list)

