import numpy as np
import sklearn.preprocessing as preprocessing
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from scipy.spatial.distance import hamming
from sklearn.externals import joblib
import csv
import matplotlib.pyplot as plt
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


    # plot
    print 'Gradient Boosting Decision Tree 100:'
    print 'Predicting out of sample... '
    rf = joblib.load("./models/gbdt100.pkl")
    imp = joblib.load("./models/imputer.pkl")
    scaler = joblib.load("./models/scaler.pkl")
    enc = joblib.load("./models/encoder.pkl")

    evaluator = ModelEvaluator(
        imputer=imp, scaler=scaler,
        encoder=enc, model=rf
    )
    y_pred = evaluator.predict(X_num, X_cat)

    print 'plotting...'
    prob1 = evaluator.predict_proba(X_num, X_cat)[:,1]
    fpr,tpr,thresholds = roc_curve(y, prob1, sample_weight=w)
    plt.plot(fpr,tpr,'r-',label='gbdt100')
    print




    print 'Logistic Regression:'
    print 'Predicting out of sample... '
    rf = joblib.load("./models/logistic.pkl")
    imp = joblib.load("./models/imputer.pkl")
    scaler = joblib.load("./models/scaler.pkl")
    enc = joblib.load("./models/encoder.pkl")

    evaluator = ModelEvaluator(
        imputer=imp, scaler=scaler,
        encoder=enc, model=rf
    )
    y_pred = evaluator.predict(X_num, X_cat)

    print 'plotting...'
    prob1 = evaluator.predict_proba(X_num, X_cat)[:,1]
    fpr,tpr,thresholds = roc_curve(y, prob1, sample_weight=w)
    plt.plot(fpr,tpr,'b-',label='logistic')




    print 'Gradient Boostint Decision Tree 10:'
    print 'Predicting out of sample... '
    rf = joblib.load("./models/gbdt10.pkl")
    imp = joblib.load("./models/imputer.pkl")
    scaler = joblib.load("./models/scaler.pkl")
    enc = joblib.load("./models/encoder.pkl")

    evaluator = ModelEvaluator(
        imputer=imp, scaler=scaler,
        encoder=enc, model=rf
    )
    y_pred = evaluator.predict(X_num, X_cat)

    print 'plotting...'
    prob1 = evaluator.predict_proba(X_num, X_cat)[:,1]
    fpr,tpr,thresholds = roc_curve(y, prob1, sample_weight=w)
    plt.plot(fpr,tpr,'b-',label='gbdt10')    



    plt.legend()
    plt.savefig("./test.png")
