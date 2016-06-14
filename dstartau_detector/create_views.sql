CREATE VIEW temp_dstartau_detector_eid AS 
SELECT eid FROM sample_assignments_sigmc WHERE sample_type = :sample_type;

CREATE VIEW temp_dstartau_detector_meta AS
SELECT * FROM 
  (temp_dstartau_detector_eid INNER JOIN event_labels_sigmc USING (eid))
  INNER JOIN 
  event_weights_sigmc
  USING (eid);

CREATE VIEW temp_dstartau_detector_sample AS
SELECT * FROM 
  temp_dstartau_detector_meta
  INNER JOIN
  candidate_optimized_events_sigmc
  USING (eid);
