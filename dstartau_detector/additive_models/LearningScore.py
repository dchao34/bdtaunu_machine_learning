import numpy as np
from sklearn.metrics import roc_auc_score

class learning_curve:
	#class used to obtain learning_curve.
	"""
	This class is used to plot learning_curve
	"""

	def __init__(self,
				 tran_X,
				 tran_y,
				 tran_w,
				 pred_X,
				 pred_y,
				 pred_w,
				 model,
				 train_sizes=[0.001,0.01,0.05,0.1,0.4,0.7,1]):
		self.tran_X = tran_X
		self.tran_y = tran_y
		self.tran_w = tran_w

		self.pred_X = pred_X
		self.pred_y = pred_y
		self.pred_w = pred_w

		self.model = model
		self.train_sizes = train_sizes


	def subsample(self, fraction):
		train_length = len(self.tran_X)
		resample_length = int(round(train_length * fraction))
		resample_index = np.random.choice(train_length, resample_length)
		return self.tran_X[resample_index], self.tran_y[resample_index],self.tran_w[resample_index]


	def train(self, X_train, y_train, w_train):
		self.model.fit(X_train, y_train)
		#train_err = self.model.score(X_train,y_train,w_train)
		#test_err = self.model.score(self.pred_X,self.pred_y,self.pred_w)
		prob1_train = self.model.predict_proba(X_train)[:,1]
		train_score = roc_auc_score(y_train, prob1_train)
		prob1_test = self.model.predict_proba(self.pred_X)[:,1]
		test_score = roc_auc_score(self.pred_y, prob1_test)

		return train_score,test_score

	def learning_curve(self):
		train_list = []
		test_list = []

		for fraction in self.train_sizes:
			X_train,y_train,w_train = self.subsample(fraction)
			train_score, test_score = self.train(X_train,y_train,w_train)
			train_list.append(train_score)
			test_list.append(test_score)

		return self.train_sizes, train_list, test_list









