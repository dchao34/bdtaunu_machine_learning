import sys
import time
import psycopg2
import numpy as np
import sklearn.preprocessing as preprocessing
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib

from SqlDataLoader import SqlDataLoader
from LearningDataAdapter import LearningDataAdapter
from ModelEvaluator import ModelEvaluator

if __name__ == '__main__':

    print
    print 'Loading models.'
    imp = joblib.load('models/imputer.pkl')
    scaler = joblib.load('models/scaler.pkl')
    enc = joblib.load('models/encoder.pkl')
    rf = joblib.load('models/rf.pkl')
    evaluator = ModelEvaluator(imputer=imp, scaler=scaler, encoder=enc, model=rf)
    adapter = LearningDataAdapter(for_learning=False)
    print

    # 347778957 rows in Candidate table.
    print 'Predicting and updating.'
    print 'Started on {0}'.format(time.ctime(time.time()))
    with SqlDataLoader(database='testing',
                       table_name='upsilon_candidates_sigmc',
                       itersize=200000,
                       arraysize=200000,
                       rollback=False,
                       debug=False) as sql_loader:
        sql_loader.start()
        while sql_loader.curr_records:
            sys.stdout.write('.')
            sys.stdout.flush()
            adapter.adapt_records(sql_loader.curr_records)
            score = evaluator.predict_proba(adapter.X_num, adapter.X_cat)
            sql_loader.update(adapter.record_id, score[:,1])
            sql_loader.fetch_next()
        sys.stdout.write('Done.\n')

        sql_loader.finish()
        print 'Finished on {0}'.format(time.ctime(time.time()))
        print
