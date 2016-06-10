import numpy as np
import sklearn.preprocessing as preprocessing
from sklearn.ensemble import RandomForestClassifier
from scipy.spatial.distance import hamming
from sklearn.externals import joblib
from LearningDataAdapter import LearningDataAdapter
from ModelEvaluator import ModelEvaluator

if __name__ ==  '__main__':

    print 'Importing training data... '

    adapter = LearningDataAdapter(for_learning=True)
    adapter.adapt_file('data/train.csv')
    X_num, X_cat = adapter.X_num, adapter.X_cat
    y = adapter.y

    print 'Fitting preprocessors... '

    # Imputer
    imp = preprocessing.Imputer(
        missing_values='NaN', strategy='mean', axis=0
    )
    imp.fit(X_num)
    X_num_trans = imp.transform(X_num)
    joblib.dump(imp, 'models/imputer.pkl')

    # Scaler
    scaler = preprocessing.StandardScaler(
        with_mean=True,
        with_std=True
    )
    scaler.fit(X_num_trans)
    X_num_trans = scaler.transform(X_num_trans)
    joblib.dump(scaler, 'models/scaler.pkl')

    # Categorical encoder
    enc = preprocessing.OneHotEncoder(
        n_values='auto',
        sparse=False
    )
    enc.fit(X_cat)
    X_cat_trans = enc.transform(X_cat)
    joblib.dump(enc, 'models/encoder.pkl')

    X_trans = np.hstack((X_num_trans, X_cat_trans))

    print 'Training model... '
    #rf = RandomForestClassifier(n_estimators=10)
    #rf = RandomForestClassifier(n_estimators=100)
    rf = RandomForestClassifier(n_estimators=1000)
    #rf.fit(X_trans, y, sample_weight=w)
    rf.fit(X_trans, y)
    joblib.dump(rf, 'models/rf.pkl')
    print

    print 'Predicting in sample... '
    evaluator = ModelEvaluator(
        imputer=imp, scaler=scaler,
        encoder=enc, model=rf
    )
    y_pred = evaluator.predict(X_num, X_cat)

    #print 'Training Error = {0}'.format(np.sum(w[y != y_pred]) / np.sum(w))
    print 'Training Error = {0}'.format(y_pred[y != y_pred].shape[0] / float(y_pred.shape[0]))
    print 'Predicted +, - counts = {0}, {1}'.format(y_pred[y_pred==1].shape[0], y_pred[y_pred==0].shape[0])
    print

    print 'Importing test sample... '
    adapter = LearningDataAdapter(for_learning=True)
    adapter.adapt_file('data/validate.csv')
    X_num, X_cat = adapter.X_num, adapter.X_cat
    w, y = adapter.w, adapter.y
    print

    print 'Predicting out of sample... '
    y_pred = evaluator.predict(X_num, X_cat)
    #print 'Testing Error = {0}'.format(np.sum(w[y != y_pred]) / np.sum(w))
    print 'Testing Error = {0}'.format(y_pred[y != y_pred].shape[0] / float(y_pred.shape[0]))
    print 'Predicted +, - counts = {0}, {1}'.format(y_pred[y_pred==1].shape[0], y_pred[y_pred==0].shape[0])
    print
