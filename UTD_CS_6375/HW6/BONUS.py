
import torch.nn as nn
import torch.nn.functional as F
import torch
from tqdm import tqdm

###################################################################################
#######################          NEURAL NETWORK            ########################
###################################################################################
from torch import optim
import pickle

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(10, 4)
        self.fc2_1 = nn.Linear(2, 1)
        self.fc2_2 = nn.Linear(2, 1)
        self.fc3 = nn.Linear(2, 1)

    def forward(self, x):
        x = F.sigmoid(self.fc1(x))
        x = torch.cat((F.sigmoid(self.fc2_1(x[:, 0:2])), F.sigmoid(self.fc2_2(x[:, 2:4]))), 1)
        x = self.fc3(x)
        return F.sigmoid(x)

def generate_data(M, N):
    X = torch.LongTensor(M, N).random_(2).float()
    Y = torch.zeros((M, 1))
    temp = torch.sum(X, dim=[1])
    Y[temp == 4] = 1
    Y[temp == 8] = 1
    # for i in range(M):
    #     X[i] = torch.LongTensor(N).random_(2)
    #     Y[i] = 1 if torch.sum(X[i]) == 4 or 8 else 0
    return X, Y

NN = Net().cuda()
optimizer = optim.SGD(NN.parameters(), lr=0.01)

save = {}
for i in range(3, 8):
    save[i] = {}
    M = 10**i
    N = 10
    (X, Y) = generate_data(M, N)
    X, Y = X.cuda(), Y.cuda()

    for j in tqdm(range(1000)):
        output = NN(X)
        criterion = nn.BCEWithLogitsLoss()
        loss = criterion(output, Y)
        # print(loss.item())
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()


    save[i]["fc1"] = {
        "bias": NN.fc1.bias.cpu().tolist(),
        "weight": NN.fc1.weight.cpu().tolist()
    }
    save[i]["fc2_1"] = {
        "bias": NN.fc2_1.bias.cpu().tolist(),
        "weight": NN.fc2_1.weight.cpu().tolist()
    }
    save[i]["fc2_2"] = {
        "bias": NN.fc2_2.bias.cpu().tolist(),
        "weight": NN.fc2_2.weight.cpu().tolist()
    }
    save[i]["fc3"] = {
        "bias": NN.fc3.bias.cpu().tolist(),
        "weight": NN.fc3.weight.cpu().tolist()
    }

with open("params.obj", "wb") as f:
    pickle.dump(save, f)
    # print(NN.fc1.weight)
