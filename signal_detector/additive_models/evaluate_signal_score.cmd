psql -d bdtaunuhad_lite -f create_signal_detector_inputs.sql
python score_events.py --input_table_name=temp_signal_detector_inputs_generic --output_fname=signal_scores_generic.csv --dbname=bdtaunuhad_lite
python score_events.py --input_table_name=temp_signal_detector_inputs_data --output_fname=signal_scores_data.csv --dbname=bdtaunuhad_lite
python score_events.py --input_table_name=temp_signal_detector_inputs_sigmc --output_fname=signal_scores_sigmc.csv --dbname=bdtaunuhad_lite
psql -d bdtaunuhad_lite -f drop_signal_detector_inputs.sql
