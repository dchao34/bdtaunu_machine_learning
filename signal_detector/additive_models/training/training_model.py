#! /nfs/raid13/babar/software/anaconda/bin/python
import sys
sys.path.append('/home/yunxuanli/for_yli5')

import numpy as np
import sklearn.preprocessing as preprocessing
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from scipy.spatial.distance import hamming
from sklearn.externals import joblib
import csv
import pandas as pd
from pandas import DataFrame,Series

train_x = pd.read_hdf('/home/yunxuanli/for_yli5/h5data/train_x.h5','df')
train_y = pd.read_hdf('/home/yunxuanli/for_yli5/h5data/train_y.h5','df')
train_w = pd.read_hdf('/home/yunxuanli/for_yli5/h5data/train_w.h5','df')
pred_x = pd.read_hdf('/home/yunxuanli/for_yli5/h5data/pred_x.h5','df')
pred_y = pd.read_hdf('/home/yunxuanli/for_yli5/h5data/pred_y.h5','df')
pred_w = pd.read_hdf('/home/yunxuanli/for_yli5/h5data/pred_w.h5','df')


# training
x_train = train_x.values
fraction = train_y[0].values.sum() / train_y.shape[0]
train_weight = (train_y==1)
train_weight[train_weight == 0] = fraction

rf = GradientBoostingClassifier(n_estimators=80)
rf.fit(x_train, train_y[0].values, train_weight)
joblib.dump(rf, '/home/yunxuanli/for_yli5/models/gdbt/GDBTweight80.pkl')
"""
rf = GradientBoostingClassifier(n_estimators=4)
rf.fit(x_train, train_y[0].values, train_w[0].values)
joblib.dump(rf, '/home/yunxuanli/for_yli5/models/gdbt/GDBT4.pkl')

rf = GradientBoostingClassifier(n_estimators=6)
rf.fit(x_train, train_y[0].values, train_w[0].values)
joblib.dump(rf, '/home/yunxuanli/for_yli5/models/gdbt/GDBT6.pkl')

rf = GradientBoostingClassifier(n_estimators=8)
rf.fit(x_train, train_y[0].values, train_w[0].values)
joblib.dump(rf, '/home/yunxuanli/for_yli5/models/gdbt/GDBT8.pkl')

#rf = joblib.load("GDBT100.pkl")

y_pred = rf.predict(x_train)
print 'Training Error = {0}'.format(np.sum(train_w[0].values[train_y[0].values != y_pred]) / np.sum(train_w[0].values))

x_valid = pca.transform(pred_x.values)
y_pred = rf.predict(x_valid)
print 'Testing Error = {0}'.format(np.sum(pred_w[0].values[pred_y[0].values != y_pred]) / np.sum(pred_w[0].values))
"""
