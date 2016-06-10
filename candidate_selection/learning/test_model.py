import numpy as np
import sklearn.preprocessing as preprocessing
from sklearn.ensemble import RandomForestClassifier
from scipy.spatial.distance import hamming
from sklearn.externals import joblib

from LearningDataAdapter import LearningDataAdapter
from ModelEvaluator import ModelEvaluator

# Compute the absolute deviation of s from the median absolute deviation (MAD)
# of 1D ndarray scores. Return -1 if MAD is 0.
def compute_mad_dev(s, scores):
    med = np.median(scores)
    mad = np.median(np.abs(scores - med))

    mad_dev = -1
    if mad != 0:
        mad_dev = abs(s - mad) / mad

    return mad_dev


# Choose the best candidate.
def select_best_candidate(C_id, C_att):
    """
    Define the following:
    M: Number of events in the sample.
    N: Number of candidates in the sample.
    D: Number of raw features that a candidate has.
    (N >= M, since each event can have many candidates.)

    Input
    -----

        C_id: ndarray with shape (N, 2).
           Each row corresponds to a candidate and the columns are attributes
           that uniquely identify it within the sample. They are the following:
               ``eid'': Event Id this candidate belongs to.
               ``idx'': The unique integer identifier of this candidate in ``eid''.

        C_att: ndarray with shape (N, D+2). The ith row corresponds to the ith row in C_id.
           Each row corresponds to a candidate and the columns are ordered to
           correspond to the following attributes:

               First D colmuns: Candidate features that are carried along.
               ``score'': Score that assess the quality of the candidate.
               ``label'': 1 if this candidate is truth matched, 0 otherwise.

    Output
    -----

        E_id: ndarray with shape (M, 2). E_id contains a subset of rows from C_id.
           The candidates kept are those that have the highest ``score'' among all
           candidates having the same ``eid''.

        E_att: ndarray with shape (M, D+2). E_att contains a subset of rows from C_att.
            The ith row corresponds to the ith row in E_id.

        E_meta: ndarray with shape (M, 4). The ith row corresponds to the ith row in E_id.
           Each row saves the following attributes about the event, whose columns are oredered
           to correspond to the following attributes:
               ``hot'': 1 if this event actually has a truth matched candidate, 0 otherwise.
               ``n_cand'': Number of candidates ``eid'' had.
               ``n_opt'': Number of candidates in ``eid'' that had the optimal ``score''.
               ``opt_mad_dev'': Number of median absolute deviations (MAD) the optimal score
                                deviates from the median score in ``eid''.

    """

    E_id, E_att, E_meta = [], [], []
    for eid in np.unique(C_id[:, 0]):

        # Subset out candidates in eid for each input array.
        eid_mask = (C_id[:, 0] == eid)
        sub_C_id, sub_C_att = C_id[eid_mask], C_att[eid_mask]

        # Count the number of candidates in this event.
        n_cand = sub_C_id.shape[0]

        # Decide if this event has a truth matched candidate at all.
        hot = 0
        if 1.0 in np.unique(sub_C_att[:,-1]):
            hot = 1

        # Compute optimal candidate and attributes regarding the optimum.
        cand_indices, scores = sub_C_id[:, 1], sub_C_att[:,-2]
        opt_val, opt_idx = np.max(scores), np.argmax(scores)

        n_opt = np.count_nonzero(scores == opt_val)
        opt_mad_dev = compute_mad_dev(opt_val, scores)

        opt_cand_idx = cand_indices[opt_idx]
        opt_att = sub_C_att[opt_idx].tolist()

        # Put the results in the appropriate lists
        E_id.append([eid, opt_cand_idx])
        E_att.append(opt_att)
        E_meta.append([hot, n_cand, n_opt, opt_mad_dev])

    return np.array(E_id), np.array(E_att), np.array(E_meta)


def print_results(E_id, E_att, E_meta):

    # Overall characteristics
    n_events, n_hot = E_id.shape[0], np.count_nonzero(E_meta[:,0] > 0)
    print '  Number of events: {0}'.format(n_events)
    print '  Number of events with a tm candidate: {0}'.format(n_hot)
    print '  Ratio: {0}'.format(n_hot / float(n_events))
    print

    # Number of successful choices
    n_success = np.count_nonzero(E_att[:,-1] > 0)
    print '  Number of events with a tm candidate: {0}'.format(n_hot)
    print '  Number of events with successful choices: {0}'.format(n_success)
    print '  Ratio: {0}'.format(n_success / float(n_hot))
    print

if __name__ == '__main__':

    print '+ Loading pickled objects... '
    imp = joblib.load('models/imputer.pkl')
    scaler = joblib.load('models/scaler.pkl')
    enc = joblib.load('models/encoder.pkl')
    rf = joblib.load('models/rf.pkl')
    print

    print '+ Importing test sample... '
    adapter = LearningDataAdapter(for_learning=True)
    adapter.adapt_file('data/validate.csv')
    print


    print '+ Predicting test sample candidate scores... '
    evaluator = ModelEvaluator(
        imputer=imp, scaler=scaler,
        encoder=enc, model=rf
    )
    score = evaluator.predict_proba(adapter.X_num, adapter.X_cat)[:,1]
    print

    print '+ Assessing model results... '
    print

    print '  Selecting best candidate... '
    C_id = adapter.record_id
    C_att = np.hstack((
        adapter.X_num, adapter.X_cat,
        score.reshape(score.shape[0], 1),
        adapter.y.reshape(adapter.y.shape[0], 1),
    ))
    E_id, E_att, E_meta = select_best_candidate(C_id, C_att)
    print

    print_results(E_id, E_att, E_meta)

    print '+ Assessing min Eextra results... '
    print

    score = -1 * adapter.X_num[:,1]

    print '  Selecting best candidate... '
    C_id = adapter.record_id
    C_att = np.hstack((
        adapter.X_num, adapter.X_cat,
        score.reshape(score.shape[0], 1),
        adapter.y.reshape(adapter.y.shape[0], 1),
    ))
    E_id, E_att, E_meta = select_best_candidate(C_id, C_att)
    print

    print_results(E_id, E_att, E_meta)
