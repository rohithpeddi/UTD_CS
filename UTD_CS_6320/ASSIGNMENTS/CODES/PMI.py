import numpy as np
import pandas as pd

data = pd.read_csv("../HW4/PMI.csv")
M, N = data.shape

# Compute total values
total = 0
for j in range(1, data.columns.size):
    column = data.columns[j]
    column_count = data[column].sum()
    total += column_count

# Compute probabilities for each word and context
for j in range(1, data.columns.size):
    column = data.columns[j]
    data[column] = data[column]/total

words = data[data.columns[:1]].values.reshape(-1)
contexts = data.columns[1:].values

wpd = {}
cpd = {}
jpd = {}
for context in contexts:
    for i in range(M):
        jpd[(words[i], context)] = data[context][i]
        wpd[words[i]] = wpd[words[i]] + data[context][i] if words[i] in wpd else data[context][i]
        cpd[context] = cpd[context] + data[context][i] if context in cpd else data[context][i]

PMI = np.empty((M, N-1))
PPMI = np.empty((M, N-1))
for i in range(M):
    for j in range(N-1):
        word = words[i]
        context = contexts[j]
        if jpd[(word, context)] == 0:
            PMI[i][j] = -111
            PPMI[i][j] = -111
        else:    
            PMI[i][j] = np.log2(jpd[(word, context)] / (wpd[word] * cpd[context]))
            PPMI[i][j] = 0 if PMI[i][j] < 0 else PMI[i][j]

PMI_df = pd.DataFrame(PMI)
PPMI_df = pd.DataFrame(PPMI)

print(PMI_df.head())
print(PPMI_df.head())

# Alpha smoothed PMI and PPMI

alpha = 0.75

total_alpha = 0
for j in range(len(contexts)):
    total_alpha += np.power(cpd[contexts[j]], alpha)

for j in range(len(contexts)):
    cpd[contexts[j]] = np.round(np.power(cpd[contexts[j]], alpha)/total_alpha, 3)

APMI = np.empty((M, N-1))
APPMI = np.empty((M, N-1))
for i in range(M):
    for j in range(N-1):
        word = words[i]
        context = contexts[j]
        if jpd[(word, context)] == 0:
            APMI[i][j] = -111
            APPMI[i][j] = -111
        else:
            APMI[i][j] = np.log2(jpd[(word, context)] / (wpd[word] * cpd[context]))
            APPMI[i][j] = 0 if APMI[i][j] < 0 else APMI[i][j]

APMI_df = pd.DataFrame(np.round(APMI, 3))
APPMI_df = pd.DataFrame(np.round(APPMI, 3))

print(APMI_df.head())
print(APPMI_df.head())