import subprocess as sp
import tempfile
import re
import sys
import time

create_views_script = 'create_views.sql'
find_max_weight_script = 'find_max_weight.sql'
count_data_script = 'count_data.sql'
copy_data_script = 'copy_data.sql'
drop_views_script = 'drop_views.sql'


def get_weight_info(psql_command):

    match_max, match_sum = None, None
    float_matcher = re.compile('([-+]?(\d*[.])?\d+)')

    temp = tempfile.TemporaryFile(mode='w+b')
    sp.check_call(psql_command, stdout=temp)
    temp.seek(0)
    for line in temp:
        tok = line.strip().split('|')
        match_max = float_matcher.search(tok[0].strip())
        match_sum = float_matcher.search(tok[1].strip())
        if match_max:
            break
    temp.close()

    return float(match_max.group(0)), float(match_sum.group(0))

def get_row_count(psql_command):

    match = None

    temp = tempfile.TemporaryFile(mode='w+b')
    sp.check_call(psql_command, stdout=temp)
    temp.seek(0)
    for line in temp:
        match = re.search('^\d+',line.strip())
        if match:
            break
    temp.close()

    return int(match.group(0))

if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser(description='Obtain machine learning sample. ')
    parser.add_argument('sample_type', type=int,
                        help='type of machine learning sample to obtain. ')
    parser.add_argument('scale', type=float,
                        help='scale factor affecting subsampling. '
                        'higher means less subsampling. ')
    parser.add_argument('--output_fname', '-o', type=str, required=True,
                        help='file name to copy to. ')
    parser.add_argument('--dbname', '-d', type=str, required=True,
                        help='database to connect to. ')
    parser.add_argument('--estimate_counts', action='store_true',
                        help='estimate the number of records returned instead of copying. ')
    args = parser.parse_args()

    start_all = time.time()

    print '+ Querying database \'{0}\'.\n'.format(args.dbname)
    sys.stdout.flush()

    # decide the max weight and check validity of 'scale'
    start = time.time()
    print '+ Checking consistency of the undersampling scale...'
    sys.stdout.flush()
    max_weight, sum_weight = get_weight_info(
        ['psql', '-q', '-t', '-F', '|',
         '-d', args.dbname,
         '-f', find_max_weight_script])

    max_subsample_p = max_weight * args.scale / sum_weight
    print '  max_weight * scale / sum_weight = {0}.'.format(max_subsample_p)
    if max_subsample_p > 1.0:
        raise RuntimeError(
            'must have max_weight * scale / sum_weight <= 1'.format(max_subsample_p)
        )
    end = time.time()
    print '  completed in {0} seconds. \n'.format(round(end-start, 2))

    # create views
    with tempfile.TemporaryFile(mode='w+b') as temp:
        sp.check_call(
            ['psql', '-q', '-d', args.dbname,
             '-v', 'scale={0}'.format(args.scale),
             '-v', 'sample_type={0}'.format(args.sample_type),
             '-f', create_views_script],
            stdout=temp)

    # count records to return
    if args.estimate_counts:
        start = time.time()
        print '+ Estimating the number of returned rows... '
        sys.stdout.flush()

        row_count = get_row_count(
            ['psql', '-q', '-d', args.dbname, '-f', count_data_script])
        print '  estimated row count: {0}'.format(row_count)
        end = time.time()
        print '  completed in {0} seconds. \n'.format(round(end-start, 2))

    # copy records to file
    if not args.estimate_counts:
        start = time.time()
        print '+ Copying rows to file \'{0}\'... '.format(args.output_fname)
        sys.stdout.flush()

        with open(args.output_fname, 'w') as w:
            sp.check_call(
                ['psql', '-q', '-d', args.dbname,
                '-f', copy_data_script],
                stdout=w)
        end = time.time()
        print '  completed in {0} seconds. \n'.format(round(end-start, 2))

    # drop views
    with tempfile.TemporaryFile(mode='w+b') as temp:
        sp.check_call(
            ['psql', '-q', '-d', args.dbname, '-f', drop_views_script],
            stdout=temp)

    print '+ done. completed in {0} seconds. \n'.format(round(end-start_all, 2))
