import sys
import subprocess
import time

dbname = 'bdtaunuhad_lite'
executable_path = '../assign_candidate_selection_mclabels'
executable_cfg = 'assign_candidate_selection_mclabels_template.cfg'
populate_sql_script = 'populate_candidate_selection_mclabels.sql' 

start_all = time.time()

print "assigning labels... "
sys.stdout.flush()
start = time.time()
subprocess.check_call([executable_path, executable_cfg])
end = time.time()
print "completed in {0} seconds. \n".format(round(end-start, 2))
sys.stdout.flush()

print "populating database... "
sys.stdout.flush()
start = time.time()
subprocess.check_call(["psql", "-d", dbname, "-f" , populate_sql_script])
end = time.time()
print "completed in {0} seconds. \n".format(round(end-start, 2))
sys.stdout.flush()

print "done. total runtime: {0}\n".format(round(end-start_all, 2))
