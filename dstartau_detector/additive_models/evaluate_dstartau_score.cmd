psql -d bdtaunuhad_lite -f create_dstartau_detector_inputs.sql
python score_events.py --input_table_name=temp_dstartau_detector_inputs_generic --output_fname=dstartau_scores_generic.csv --dbname=bdtaunuhad_lite
python score_events.py --input_table_name=temp_dstartau_detector_inputs_data --output_fname=dstartau_scores_data.csv --dbname=bdtaunuhad_lite
python score_events.py --input_table_name=temp_dstartau_detector_inputs_sigmc --output_fname=dstartau_scores_sigmc.csv --dbname=bdtaunuhad_lite
psql -d bdtaunuhad_lite -f drop_dstartau_detector_inputs.sql
