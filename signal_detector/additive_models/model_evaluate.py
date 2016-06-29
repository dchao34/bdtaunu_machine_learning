import numpy as np
import sklearn.preprocessing as preprocessing
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from scipy.spatial.distance import hamming
from sklearn.externals import joblib
import csv
from LearningDataAdapter import LearningDataAdapter
from ModelEvaluator import ModelEvaluator
from sklearn.metrics import roc_curve

if __name__ ==  '__main__':
	
	plt.switch_backend('agg')


	# obtain valid data
	print 'Importing test sample... '
    adapter = LearningDataAdapter(for_learning=True)
    adapter.adapt_file('data/validate.csv')
    X_num, X_cat = adapter.X_num, adapter.X_cat
    w, y = adapter.w, adapter.y
    print


	rf = joblib.load("./models/GDBTc80.pkl")
	print 'Predicting in sample... '
	evaluator = ModelEvaluator(
	    imputer=imp, scaler=scaler,
	    encoder=enc, model=rf
	)
	y_pred = evaluator.predict(X_num, X_cat)
	prob1 = rf.predict_proba(x_valid)[:,1]
	fpr,tpr,thresholds = roc_curve(pred_y[0].values, prob1, sample_weight=pred_w[0].values)
	plt.plot(fpr,tpr,'r-',label='GDBTc80')
	

	rf = joblib.load("./models/logistic.pkl")
	print 'Predicting in sample... '
	evaluator = ModelEvaluator(
	    imputer=imp, scaler=scaler,
	    encoder=enc, model=rf
	)
	y_pred = evaluator.predict(X_num, X_cat)
	prob1 = rf.predict_proba(x_valid)[:,1]
	fpr,tpr,thresholds = roc_curve(pred_y[0].values, prob1, sample_weight=pred_w[0].values)
	plt.plot(fpr,tpr,'r-',label='logistic')


	plt.legend()
	plt.savefig("./test.png")


"""
for i in [10,40,80]:
	path = "/home/yunxuanli/for_yli5/models/gdbt/GDBTc" + str(i) + ".pkl"
	rf = joblib.load(path)
	#y_pred = rf.predict(x_train)
	#print 'Training Error = {0}'.format(np.sum(train_w[0].values[train_y[0].values != y_pred]) / np.sum(train_w[0].values))
	y_pred = rf.predict(x_valid)
	#print 'Testing Error = {0}'.format(np.sum(pred_w[0].values[pred_y[0].values != y_pred]) / np.sum(pred_w[0].values))
	#true_false = 0
	#for i in range(len(y_pred)-1):
	#    if(y_pred[i] == 0 and pred_y[0].values[i] == 1):
	#true_false = true_false + pred_w[0].values[i]
	#print 'True->False rate = {0}'.format(true_false/np.sum(train_w[0].values))

	#false_true = 0
	#for i in range(len(y_pred)-1):
	#    if(y_pred[i] == 1 and pred_y[0].values[i] == 0):
	#        false_true = false_true + pred_w[0].values[i]
	#print 'False->True rate = {0}'.format(false_true/np.sum(train_w[0].values))

	prob1 = rf.predict_proba(x_valid)[:,1]
	fpr,tpr,thresholds = roc_curve(pred_y[0].values, prob1, sample_weight=pred_w[0].values)
	Label = "GDBTc" + str(i)
	plt.plot(fpr,tpr,'g-',label=Label)

#GDBT weight
rf = joblib.load("/home/yunxuanli/for_yli5/models/gdbt/GDBTweight30.pkl")
y_pred = rf.predict(x_valid)
prob1 = rf.predict_proba(x_valid)[:,1]
fpr,tpr,thresholds = roc_curve(pred_y[0].values, prob1, sample_weight=pred_w[0].values)
plt.plot(fpr,tpr,'r-',label='GDBTweight30')

rf = joblib.load("/home/yunxuanli/for_yli5/models/gdbt/GDBTweight80.pkl")
y_pred = rf.predict(x_valid)
prob1 = rf.predict_proba(x_valid)[:,1]
fpr,tpr,thresholds = roc_curve(pred_y[0].values, prob1, sample_weight=pred_w[0].values)
plt.plot(fpr,tpr,'r-',label='GDBTweight80')


#random forest
rf = joblib.load("/home/yunxuanli/for_yli5/models/rf/rf10.pkl")
y_pred = rf.predict(x_valid)
prob1 = rf.predict_proba(x_valid)[:,1]
fpr,tpr,thresholds = roc_curve(pred_y[0].values, prob1, sample_weight=pred_w[0].values)
plt.plot(fpr,tpr,'b-',label='rf10')

rf = joblib.load("/home/yunxuanli/for_yli5/models/rf/rf100.pkl")
y_pred = rf.predict(x_valid)
prob1 = rf.predict_proba(x_valid)[:,1]
fpr,tpr,thresholds = roc_curve(pred_y[0].values, prob1, sample_weight=pred_w[0].values)
plt.plot(fpr,tpr,'b-',label='rf100')

rf = joblib.load("/home/yunxuanli/for_yli5/models/rf/rf1000.pkl")
y_pred = rf.predict(x_valid)
prob1 = rf.predict_proba(x_valid)[:,1]
fpr,tpr,thresholds = roc_curve(pred_y[0].values, prob1, sample_weight=pred_w[0].values)
plt.plot(fpr,tpr,'b-',label='rf1000')


#logistic regression
rf = joblib.load("/home/yunxuanli/for_yli5/models/logre/logistic.pkl")
y_pred = rf.predict(x_valid)
prob1 = rf.predict_proba(x_valid)[:,1]
fpr,tpr,thresholds = roc_curve(pred_y[0].values, prob1, sample_weight=pred_w[0].values)
plt.plot(fpr,tpr,'k-',label='logistic')


plt.legend()
plt.savefig("/home/yunxuanli/for_yli5/models/gdbt/roc_gdbt_rf_log.png")


rf = joblib.load("GDBTc4.pkl")
print 'GDBT4'
y_pred = rf.predict(x_train)
print 'Training Error = {0}'.format(np.sum(train_w[0].values[train_y[0].values != y_pred]) / np.sum(train_w[0].values))
y_pred = rf.predict(x_valid)
print 'Testing Error = {0}'.format(np.sum(pred_w[0].values[pred_y[0].values != y_pred]) / np.sum(pred_w[0].values))


rf = joblib.load("GDBTc6.pkl")
print 'GDBT6'
y_pred = rf.predict(x_train)
print 'Training Error = {0}'.format(np.sum(train_w[0].values[train_y[0].values != y_pred]) / np.sum(train_w[0].values))
y_pred = rf.predict(x_valid)
print 'Testing Error = {0}'.format(np.sum(pred_w[0].values[pred_y[0].values != y_pred]) / np.sum(pred_w[0].values))


rf = joblib.load("GDBTc8.pkl")
print 'GDBT8'
y_pred = rf.predict(x_train)
print 'Training Error = {0}'.format(np.sum(train_w[0].values[train_y[0].values != y_pred]) / np.sum(train_w[0].values))
y_pred = rf.predict(x_valid)
print 'Testing Error = {0}'.format(np.sum(pred_w[0].values[pred_y[0].values != y_pred]) / np.sum(pred_w[0].values))


rf = joblib.load("GDBTc10.pkl")
print 'GDBT10'
y_pred = rf.predict(x_train)
print 'Training Error = {0}'.format(np.sum(train_w[0].values[train_y[0].values != y_pred]) / np.sum(train_w[0].values))
y_pred = rf.predict(x_valid)
print 'Testing Error = {0}'.format(np.sum(pred_w[0].values[pred_y[0].values != y_pred]) / np.sum(pred_w[0].values))


rf = joblib.load("GDBTc20.pkl")
print 'GDBT20'
y_pred = rf.predict(x_train)
print 'Training Error = {0}'.format(np.sum(train_w[0].values[train_y[0].values != y_pred]) / np.sum(train_w[0].values))
y_pred = rf.predict(x_valid)
print 'Testing Error = {0}'.format(np.sum(pred_w[0].values[pred_y[0].values != y_pred]) / np.sum(pred_w[0].values))


rf = joblib.load("GDBTc30.pkl")
print 'GDBT30'
y_pred = rf.predict(x_train)
print 'Training Error = {0}'.format(np.sum(train_w[0].values[train_y[0].values != y_pred]) / np.sum(train_w[0].values))
y_pred = rf.predict(x_valid)
print 'Testing Error = {0}'.format(np.sum(pred_w[0].values[pred_y[0].values != y_pred]) / np.sum(pred_w[0].values))


rf = joblib.load("GDBTc40.pkl")
print 'GDBT40'
y_pred = rf.predict(x_train)
print 'Training Error = {0}'.format(np.sum(train_w[0].values[train_y[0].values != y_pred]) / np.sum(train_w[0].values))
y_pred = rf.predict(x_valid)
print 'Testing Error = {0}'.format(np.sum(pred_w[0].values[pred_y[0].values != y_pred]) / np.sum(pred_w[0].values))


rf = joblib.load("GDBTc50.pkl")
print 'GDBT50'
y_pred = rf.predict(x_train)
print 'Training Error = {0}'.format(np.sum(train_w[0].values[train_y[0].values != y_pred]) / np.sum(train_w[0].values))
y_pred = rf.predict(x_valid)
print 'Testing Error = {0}'.format(np.sum(pred_w[0].values[pred_y[0].values != y_pred]) / np.sum(pred_w[0].values))


rf = joblib.load("GDBTc60.pkl")
print 'GDBT60'
y_pred = rf.predict(x_train)
print 'Training Error = {0}'.format(np.sum(train_w[0].values[train_y[0].values != y_pred]) / np.sum(train_w[0].values))
y_pred = rf.predict(x_valid)
print 'Testing Error = {0}'.format(np.sum(pred_w[0].values[pred_y[0].values != y_pred]) / np.sum(pred_w[0].values))


rf = joblib.load("GDBTc70.pkl")
print 'GDBT70'
y_pred = rf.predict(x_train)
print 'Training Error = {0}'.format(np.sum(train_w[0].values[train_y[0].values != y_pred]) / np.sum(train_w[0].values))
y_pred = rf.predict(x_valid)
print 'Testing Error = {0}'.format(np.sum(pred_w[0].values[pred_y[0].values != y_pred]) / np.sum(pred_w[0].values))


rf = joblib.load("GDBTc80.pkl")
print 'GDBT80'
y_pred = rf.predict(x_train)
print 'Training Error = {0}'.format(np.sum(train_w[0].values[train_y[0].values != y_pred]) / np.sum(train_w[0].values))
y_pred = rf.predict(x_valid)
print 'Testing Error = {0}'.format(np.sum(pred_w[0].values[pred_y[0].values != y_pred]) / np.sum(pred_w[0].values))
"""

