import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mutual_info_score
from scipy.stats import pearsonr
import csv

plt.switch_backend('agg')

print 'Importing training data...'
with open('./data/train.csv') as f_train:
	f_iter = csv.reader(f_train,delimiter=',')
	data_list = [i for i in f_iter]

data_np = np.array(data_list[1:],dtype=float)
feature_name = data_list[0]

label = data_np[:,-1]
for i in range(len(label)):
	if (label[i] in [11445, 11447]):
		label[i] = 1
	else:
		label[i] = 0


print 'Calculate Information Gain...'
mutual = []
correlation = []
for i in range(len(feature_name)):
	mutual_info = mutual_info_score(data_np[:,i],label)
	corr_info = abs(pearsonr(data_np[:,i],label)[0])
	mutual.append(mutual_info)
	correlation.append(corr_info)


#plot
print 'mutual 1 is '
print mutual[0]
print
print 'cor 1 is '
print correlation[0]
print
x = range(len(mutual))
plt.figure(1,figsize=(15,8))
plt.plot(x,mutual,'b-o',label='mutual')
plt.plot(x,correlation,'r-o',label='pearson')
plt.xticks(x, feature_name, rotation='vertical')
plt.subplots_adjust(bottom=0.5)
plt.legend()
plt.savefig('relative_importance.png')

