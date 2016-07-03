import sys
import time
import psycopg2
import subprocess as sp
import numpy as np
import sklearn.preprocessing as preprocessing
from sklearn.externals import joblib

from PsqlReader import PsqlReader
from LearningDataAdapter import LearningDataAdapter
from ModelEvaluator import ModelEvaluator

def LoadModelEvaluator(
    imputer_fname,  scaler_fname,
    encoder_fname, model_fname):

    imp = joblib.load(imputer_fname)
    scaler = joblib.load(scaler_fname)
    enc = joblib.load(encoder_fname)
    model = joblib.load(model_fname)
    evaluator = ModelEvaluator(imputer=imp, scaler=scaler,
                               encoder=enc, model=model)

    return evaluator

if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser(description='Predict signal score. ')
    parser.add_argument('--input_table_name', type=str, required=True,
                        help='input candidate optimized event table name. ')
    parser.add_argument('--output_fname', type=str, required=True,
                        help='input candidate optimized event table name. ')
    parser.add_argument('--dbname', '-d', type=str, required=True,
                        help='database to connect to. ')
    args = parser.parse_args()

    print
    print '+ Connecting to {0} to populate column in table {1}'.format(args.dbname, args.input_table_name)
    print

    print '  Loading models.'
    logre_evaluator = LoadModelEvaluator(
        'models/logre_imputer.pkl', 'models/logre_scaler.pkl',
        'models/logre_encoder.pkl', 'models/logre.pkl')
    adapter = LearningDataAdapter(for_learning=False)
    print

    f = open(args.output_fname, 'w')
    f.write('eid,logre_signal_score\n')

    print '  Predicting and updating.'
    print '  Started on {0}'.format(time.ctime(time.time()))
    with PsqlReader(database=args.dbname,
                    select_table_name=args.input_table_name,
                    itersize=200000,
                    arraysize=200000,
                    rollback=False,
                    debug=False) as sql_loader:
        sql_loader.start()
        while sql_loader.curr_records:
            sys.stdout.write('.')
            sys.stdout.flush()

            adapter.adapt_records(sql_loader.curr_records)

            logre_score = logre_evaluator.predict_proba(adapter.X_num, adapter.X_cat)

            for i in range(adapter.record_id.shape[0]):
                row = [ adapter.record_id[i,0] ]
                row += [ logre_score[i, 1] ]
                f.write(','.join(map(str, row)) + '\n')

            sql_loader.fetch_next()
        sys.stdout.write('Done.\n')

        sql_loader.finish()
        print '  Finished on {0}'.format(time.ctime(time.time()))
        print

    f.close()
