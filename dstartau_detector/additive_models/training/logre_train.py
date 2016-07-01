import numpy as np
import sklearn.preprocessing as preprocessing
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from scipy.spatial.distance import hamming
from sklearn.externals import joblib
from LearningDataAdapter import LearningDataAdapter
from ModelEvaluator import ModelEvaluator

if __name__ ==  '__main__':

    # data preprocessing

    print 'Importing training data... '
    adapter = LearningDataAdapter(for_learning=True)
    adapter.adapt_file('../data/train.csv')
    X_num, X_cat = adapter.X_num, adapter.X_cat
    w, y = adapter.w, adapter.y

    print 'Fitting preprocessors... '

    # Imputer
    imp = preprocessing.Imputer(
        missing_values='NaN', strategy='mean', axis=0
    )
    imp.fit(X_num)
    X_num_trans = imp.transform(X_num)
    joblib.dump(imp, '../models/imputer.pkl')

    # Scaler
    scaler = preprocessing.StandardScaler(
        with_mean=True,
        with_std=True
    )
    scaler.fit(X_num_trans)
    X_num_trans = scaler.transform(X_num_trans)
    joblib.dump(scaler, '../models/scaler.pkl')

    # Categorical encoder
    enc = preprocessing.OneHotEncoder(
        n_values='auto',
        sparse=False
    )
    enc.fit(X_cat)
    X_cat_trans = enc.transform(X_cat)
    joblib.dump(enc, '../models/encoder.pkl')

    X_trans = np.hstack((X_num_trans, X_cat_trans))


    # training

    print 'Training logistic regression...'
    rf = LogisticRegression()
    rf.fit(X_trans, y)
    joblib.dump(rf, '../models/logistic.pkl')
