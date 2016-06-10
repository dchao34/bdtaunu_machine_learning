import numpy as np

class LearningDataAdapter:
    """
    This class reads and processes candidate records whose columns are
    organized in the followinging order:

        0, 0: eid,
        1, 1: cidx,

        2, 0: mmiss2prime,
        3, 1: eextra,
        4, 2: tag_lp3,
        5, 3: tag_cosby,
        6, 4: tag_costhetadl,
        7, 5: tag_dmass,
        8, 6: tag_deltam,
        9, 7: tag_costhetadsoft,
        10, 8: tag_softp3magcm,
        11, 9: sig_hp3,
        12, 10: sig_cosby,
        13, 11: sig_costhetadtau,
        14, 12: sig_vtxb,
        15, 13: sig_dmass,
        16, 14: sig_deltam,
        17, 15: sig_costhetadsoft,
        18, 16: sig_softp3magcm,
        19, 17: sig_hmass,
        20, 18: sig_vtxh,

        21, 0: tag_isbdstar,
        22, 1: sig_isbdstar,
        23, 2: tag_dmode,
        24, 3: tag_dstarmode,
        25, 4: sig_dmode,
        26, 5: sig_dstarmode,

        27, 0: is_matched

    (last column available only if it is Monte Carlo)

    """

    # Class attributes
    # ----------------

    # Record index ranges for each attribute type
    id_first_idx, id_last_idx = 0, 1
    num_first_idx, num_last_idx = 2, 20
    cat_first_idx, cat_last_idx = 21, 26
    weight_idx = None
    label_idx = 27
    record_id_ncols = id_last_idx - id_first_idx + 1
    num_ncols = num_last_idx - num_first_idx + 1
    cat_ncols = cat_last_idx - cat_first_idx + 1

    # Specify the missing value code for numerical attributes.
    # The order is 2-20 => 0-18
    num_missval_arr = np.array([
        -999, -999, -1, -999, -999, -1, -1, -999, -1,
        -1, -999, -999, -1, -1, -1, -999, -1, -1, -1
    ])

    def __init__(self, for_learning):

        # Object attributes
        # -----------------

        self.for_learning = for_learning

        # These are 2D numpy arrays
        self.record_id = None
        self.X_num = None
        self.X_cat = None
        self.w = None
        self.y = None

        return


    def adapt_records(self, record_list):

        id_list, num_list, cat_list = [], [], []
        w_list, y_list = [], []
        for record in record_list:
            id_list.append(map(int, record[LearningDataAdapter.id_first_idx:
                                           LearningDataAdapter.id_last_idx+1]))
            num_list.append(map(float, record[LearningDataAdapter.num_first_idx:
                                              LearningDataAdapter.num_last_idx+1]))
            cat_list.append(map(int, record[LearningDataAdapter.cat_first_idx:
                                            LearningDataAdapter.cat_last_idx+1]))

            if self.for_learning:

                if LearningDataAdapter.weight_idx:
                    w_list.append(float(record[LearningDataAdapter.weight_idx]))

                if float(record[LearningDataAdapter.label_idx]) == -1:
                    y_list.append(0.0)
                else:
                    y_list.append(1.0)

        id_arr = np.array(id_list).reshape(len(id_list),
                                           LearningDataAdapter.record_id_ncols)
        num_arr = np.array(num_list).reshape(len(num_list),
                                             LearningDataAdapter.num_ncols)
        cat_arr = np.array(cat_list).reshape(len(cat_list),
                                             LearningDataAdapter.cat_ncols)

        w_arr = np.array(w_list)

        y_arr = np.array(y_list)

        # Fill missing values for numeric attributes
        for i, miss_val in enumerate(LearningDataAdapter.num_missval_arr):
            miss_mask = (num_arr[:,i] == miss_val)
            num_arr[:,i][miss_mask] = np.nan


        # Deduce alternative encoding of categorical attributes

        # 0: tag_dtype. Recode -1, 3, 6 -> 0
        cat_mask = (cat_arr[:,2] == -1) | (cat_arr[:,2] == 3) | (cat_arr[:,2] == 6)
        cat_arr[:,2][cat_mask] = 0

        # 2: sig_dtype. Recode -1, 3, 6 -> 0
        cat_mask = (cat_arr[:,4] == -1) | (cat_arr[:,4] == 3) | (cat_arr[:,4] == 6)
        cat_arr[:,4][cat_mask] = 0

        # 1: tag_dstartype. Recode -1 -> 0
        cat_mask = (cat_arr[:,3] == -1)
        cat_arr[:,3][cat_mask] = 0

        # 3: sig_dstartype. Recode -1 -> 0
        cat_mask = (cat_arr[:,5] == -1)
        cat_arr[:,5][cat_mask] = 0

        self.record_id = id_arr
        self.X_num = num_arr
        self.X_cat = cat_arr
        self.w = w_arr
        self.y = y_arr

        return

    def adapt_file(self, fname):
        records_list = []
        with open(fname, 'r') as f:
            next(f)
            for line in f:
                records_list.append(line.strip().split(','))
        self.adapt_records(records_list)
        return


if __name__ == '__main__':

    adapter = LearningDataAdapter(True)

    adapter.adapt_file('data/train.csv')

    X = np.hstack((adapter.X_num, adapter.X_cat))
    print X
    print
    print X[0]
    print X[500]
    print X[-1]
    print
    print X.shape
