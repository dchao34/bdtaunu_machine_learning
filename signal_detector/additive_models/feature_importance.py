import numpy as np
import csv

if __name__ == '__main__':
	print 'Importing training data...'
	with open('./data/train.csv') as f_train:
		f_iter = csv.reader(f_train,delimiter=',')
		data_list = [i for i in f_iter]
	data_np = np.array(data_list[1:],dtype=object)
	feature_name = data_list[0,:]

	print data_np.shape
	print '---'
	print feature_name