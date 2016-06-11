import sys
import time
import psycopg2
import subprocess as sp
import numpy as np
import sklearn.preprocessing as preprocessing
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib

from SqlDataLoader import SqlDataLoader
from LearningDataAdapter import LearningDataAdapter
from ModelEvaluator import ModelEvaluator

def add_table_column(dbname, table_name):
    alter_template = 'ALTER TABLE {0} ADD COLUMN cand_score real;'
    alter_query = alter_template.format(table_name)
    status = sp.check_call(['psql', '-q', '-d', dbname,
                            '-c', alter_query])
    return


if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser(description='Score upsilon candidates. ')
    parser.add_argument('--table_name', '-t', type=str, required=True,
                        help='candidate table name. ')
    parser.add_argument('--dbname', '-d', type=str, required=True,
                        help='database to connect to. ')
    args = parser.parse_args()

    print
    print '+ Connecting to {0} to populate column in table {1}'.format(args.dbname, args.table_name)
    print

    print '  Adding new column to table.'
    add_table_column(args.dbname, args.table_name)
    print

    print '  Loading models.'
    imp = joblib.load('models/imputer.pkl')
    scaler = joblib.load('models/scaler.pkl')
    enc = joblib.load('models/encoder.pkl')
    rf = joblib.load('models/rf.pkl')
    evaluator = ModelEvaluator(imputer=imp, scaler=scaler, encoder=enc, model=rf)
    adapter = LearningDataAdapter(for_learning=False)
    print

    print '  Predicting and updating.'
    print '  Started on {0}'.format(time.ctime(time.time()))
    with SqlDataLoader(database=args.dbname,
                       table_name=args.table_name,
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
        print '  Finished on {0}'.format(time.ctime(time.time()))
        print
