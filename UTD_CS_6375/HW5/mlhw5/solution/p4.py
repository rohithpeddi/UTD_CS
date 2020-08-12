# coding:utf-8
import numpy as np
from copy import deepcopy

def import_data(fname):
	fh = open(fname,'r')
	content = fh.readlines()
	fh.close()
	X=[];Y=[]
	for line in content:
		values = line.strip().split(',')
		X.append(values[0:-1])
		Y.append(values[-1])
	X= np.array(X,dtype='float').T
	Y= np.array([Y],dtype='float')
	# map labels to +- 1
	Y = (Y-1.5)*2
	return X,Y

class GuassianNaiveBayes:
	def fit(self,X,Y):
		self.rvX_Y = {}
		self.rvY = {}
		types = np.unique(Y)
		_Y = Y[0]
		for y in types:
			self.rvY[y]=len(_Y[_Y==y])/float(Y.size)
		M,N = X.shape
		for i in range(M):
			f_i = X[i,:]
			for y in types:
				selector = _Y==y
				data = f_i[selector]
				mu=np.mean(data)
				sigma = np.sqrt(np.mean( (data-mu)**2 ))
				self.rvX_Y[i,y]=(mu,sigma)
		return

	def predict(self,X):
		M,N = X.shape
		ret = np.zeros((1,N))
		for i in range(N):
			x_i=X[:,i]
			type_prob = []

			for y in self.rvY.keys():
				prob = self.rvY[y]
				for f in range(M):
					mu,sigma=self.rvX_Y[f,y]
					prob*=(1.0/(sigma*np.sqrt(2*np.pi)))*np.exp(-0.5*((x_i[f]-mu)/sigma)**2)
				type_prob.append((y,prob))
			type_prob.sort(key = lambda x:x[1],reverse=True)

			ret[0,i]=type_prob[0][0]
		return ret

	def evaluate(self,X,Y):
		tags = self.predict(X)
		n_right = np.sum(tags == Y)
		accuracy = float(n_right)/Y.size
		return accuracy

if __name__ == '__main__':
	X_tr,Y_tr = import_data('../sonar_train.data')
	X_vd,Y_vd = import_data('../sonar_valid.data')
	X_ts,Y_ts = import_data('../sonar_test.data')
	gnb = GuassianNaiveBayes()
	gnb.fit(X_tr,Y_tr)
	print(gnb.evaluate(X_ts,Y_ts))