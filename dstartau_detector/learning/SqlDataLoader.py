import numpy as np
import psycopg2
import tempfile
import subprocess as sp

def deduce_column_names():

    colnames = [
        'eid',
        'cidx',
        'ntracks',
        'r2all',
        'mmiss2',
        'mmiss2prime',
        'eextra',
        'costhetat',
        'tag_lp3',
        'tag_cosby',
        'tag_costhetadl',
        'tag_dmass',
        'tag_deltam',
        'tag_costhetadsoft',
        'tag_softp3magcm',
        'sig_hp3',
        'sig_cosby',
        'sig_costhetadtau',
        'sig_vtxb',
        'sig_dmass',
        'sig_deltam',
        'sig_costhetadsoft',
        'sig_softp3magcm',
        'sig_hmass',
        'sig_vtxh',
        'cand_score',
        'signal_score',
        'tag_isbdstar',
        'sig_isbdstar',
        'tag_dmode',
        'tag_dstarmode',
        'sig_dmode',
        'sig_dstarmode',
        'tag_l_epid',
        'tag_l_mupid',
    ]

    return colnames


class SqlDataLoader:

    def __init__(self,
                 database,
                 select_table_name,
                 update_table_name,
                 itersize=2000, arraysize=1,
                 rollback=False, debug=False):

        self.conn = psycopg2.connect(database=database)
        self.select_table_name = select_table_name
        self.update_table_name = update_table_name

        self.select_cursor = None
        self.update_cursor = None

        self.itersize = itersize
        self.arraysize = arraysize
        self.rollback = rollback
        self.debug = debug

        # assemble select statement
        colnames = deduce_column_names()
        columns = ', '.join(colnames)
        self.select_stmt = 'SELECT {0} FROM {1};'.format(columns, self.select_table_name)
        if debug:
            self.select_stmt = self.select_stmt.strip(';') + ' LIMIT 10;'

        # assemble update statement
        self.update_stmt_template = 'UPDATE ' + self.update_table_name + ' SET dstartau_score = %s WHERE eid = %s;'

        return

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if self.rollback:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()
        return

    def start(self):
        self.select_cursor = self.conn.cursor('sql_data_reader')
        self.select_cursor.itersize = self.itersize
        self.select_cursor.arraysize = self.arraysize
        self.select_cursor.execute(self.select_stmt)

        self.update_cursor = self.conn.cursor()

        self.curr_records = self.select_cursor.fetchmany()
        return

    def fetch_next(self):
        self.curr_records = self.select_cursor.fetchmany()
        return

    def update(self, record_id_arr, score_arr):
        score_list, record_id_list = score_arr.tolist(), record_id_arr.tolist()
        update_list = [ (s, r[0]) for s, r in zip(score_list, record_id_list) ]
        self.update_cursor.executemany(self.update_stmt_template, update_list)
        return

    def finish(self):
        self.select_cursor.close()
        self.update_cursor.close()
        return

    def dump_csv(self, output_fname):

        stmt = self.select_stmt
        stmt = 'COPY (' + stmt.strip(';') + ') TO STDOUT WITH CSV HEADER; '

        self.select_cursor = self.conn.cursor()
        f = open(output_fname, 'w')
        self.select_cursor.copy_expert(stmt, f)
        f.close()
        self.select_cursor.close()

        return


if __name__ == '__main__':

    database = 'testing'

    sp.check_call(['psql', '-q', '-d', database,
                   '-f', 'create_dstartau_detector_inputs.sql'])

    select_table_name = 'temp_dstartau_detector_inputs_generic'
    update_table_name = 'candidate_optimized_events_scores_generic'

    print 'Streaming over Candidates; not for machine learning: '
    print '---------------------------------------------------- '
    print
    with SqlDataLoader(database,
                       select_table_name,
                       update_table_name,
                       arraysize=5,
                       rollback=True, debug=True) as sql_loader:
        sql_loader.start()
        while sql_loader.curr_records:
            print 'fetched {0} row(s):'.format(len(sql_loader.curr_records))
            for row in sql_loader.curr_records:
                print row
            sql_loader.fetch_next()
            print
        sql_loader.finish()
    print
    print

    print 'Dumping CSV file; not for machine learning: '
    print '------------------------------------------ '
    with SqlDataLoader(database,
                       select_table_name,
                       update_table_name,
                       arraysize=5,
                       rollback=True, debug=True) as sql_loader:
        with tempfile.NamedTemporaryFile('r+w') as f:
            sql_loader.dump_csv(f.name)
            f.seek(0)
            for line in f:
                print line.strip()
    print
    print

    sp.check_call(['psql', '-q', '-d', database,
                   '-f', 'drop_dstartau_detector_inputs.sql'])
