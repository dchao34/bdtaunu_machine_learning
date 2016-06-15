CREATE VIEW temp_dstartau_detector_inputs_generic AS
SELECT * FROM 
  (candidate_optimized_events_generic
   INNER JOIN 
   (SELECT eid, signal_score FROM candidate_optimized_events_scores_generic) AS CES
   USING (eid));

CREATE VIEW temp_dstartau_detector_inputs_sigmc AS
SELECT * FROM 
  (candidate_optimized_events_sigmc
   INNER JOIN 
   (SELECT eid, signal_score FROM candidate_optimized_events_scores_sigmc) AS CES
   USING (eid));

CREATE VIEW temp_dstartau_detector_inputs_data AS
SELECT * FROM 
  (candidate_optimized_events_data
   INNER JOIN 
   (SELECT eid, signal_score FROM candidate_optimized_events_scores_data) AS CES
   USING (eid));
