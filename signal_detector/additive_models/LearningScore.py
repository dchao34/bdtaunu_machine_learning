import numpy as np


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
				 train_sizes=[0.2,0.4,0.6,0.8,1.0]):
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
		train_err = self.model.score(X_train,y_train,w_train)
		test_err = self.model.score(self.pred_X,self.pred_y,self.pred_w)
		return train_err,test_err

	def learning_curve(self):
		train_list = []
		test_list = []

		for fraction in self.train_sizes:
			X_train,y_train,w_train = self.subsample(fraction)
			train_err, test_err = self.train(X_train,y_train,w_train)
			train_list.append(train_err)
			test_list.append(test_err)

		return self.train_sizes, train_list, test_list









