import numpy as np
import psycopg2
import tempfile


class PsqlReader:


    def __init__(self,
                 database,
                 select_table_name,
                 itersize=2000, arraysize=1,
                 rollback=False, debug=False):

        self.conn = psycopg2.connect(database=database)
        self.select_table_name = select_table_name

        self.select_cursor = None

        self.itersize = itersize
        self.arraysize = arraysize
        self.rollback = rollback
        self.debug = debug

        # assemble select statement
        self.select_stmt = 'SELECT * FROM {0};'.format(self.select_table_name)
        if debug:
            self.select_stmt = self.select_stmt.strip(';') + ' LIMIT 10;'

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

        self.curr_records = self.select_cursor.fetchmany()
        return

    def fetch_next(self):
        self.curr_records = self.select_cursor.fetchmany()
        return


    def finish(self):
        self.select_cursor.close()
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
    select_table_name = 'candidate_optimized_events_generic'

    print 'Streaming over Candidates; not for machine learning: '
    print '---------------------------------------------------- '
    print
    with PsqlReader(database,
                    select_table_name,
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
    with PsqlReader(database,
                    select_table_name,
                    arraysize=5,
                    rollback=True, debug=True) as sql_loader:
        with tempfile.NamedTemporaryFile('r+w') as f:
            sql_loader.dump_csv(f.name)
            f.seek(0)
            for line in f:
                print line.strip()
    print
    print

