import numpy as np

class ModelEvaluator:

    def __init__(self,
                 imputer=None,
                 scaler=None,
                 encoder=None,
                 model=None):
        self.imputer = imputer
        self.scaler = scaler
        self.encoder = encoder
        self.model = model
        return

    def preprocess(self, X_num, X_cat):
        if self.imputer:
            X_num = self.imputer.transform(X_num)
        if self.scaler:
            X_num = self.scaler.transform(X_num)
        if self.encoder:
            X_cat = self.encoder.transform(X_cat)
        return np.hstack((X_num, X_cat))

    def predict_proba(self, X_num, X_cat):
        X = self.preprocess(X_num, X_cat)
        return self.model.predict_proba(X)

    def predict(self, X_num, X_cat):
        X = self.preprocess(X_num, X_cat)
       # return self.model.predict(X)
	# change by yli5 for outputting data
	return X


if __name__ == '__main__':

    from LearningDataAdapter import LearningDataAdapter
    from sklearn.externals import joblib

    print 'Loading data...'
    adapter = LearningDataAdapter(for_learning=True)
    adapter.adapt_file('data/train.csv')

    print 'Loading models...'
    imputer = joblib.load('models/imputer.pkl')
    scaler = joblib.load('models/scaler.pkl')
    encoder = joblib.load('models/encoder.pkl')
    model = joblib.load('models/rf.pkl')

    print 'Predicting...'
    evaluator = ModelEvaluator(
        imputer=imputer, scaler=scaler,
        encoder=encoder, model=model
    )

    X_num, X_cat = adapter.X_num, adapter.X_cat
    w, y = adapter.w, adapter.y

    pred = evaluator.predict(X_num, X_cat)
    print pred

    prob = evaluator.predict_proba(X_num, X_cat)
    print prob

