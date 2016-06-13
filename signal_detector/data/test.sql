CREATE TEMPORARY VIEW ml_sample_eid AS 
SELECT eid FROM sample_assignments_generic WHERE sample_type = 1;

CREATE TEMPORARY VIEW ml_sample_meta AS
SELECT * FROM 
  (ml_sample_eid INNER JOIN event_modelabels_generic USING (eid))
  INNER JOIN 
  event_weights_generic
  USING (eid);

CREATE TEMPORARY TABLE ml_sample_meta_cand AS
SELECT * FROM 
  (ml_sample_meta INNER JOIN optimal_upsilon_candidates USING (eid));
CREATE INDEX ON ml_sample_meta_cand (eid, cidx);

CREATE TEMPORARY VIEW candidate_features AS
  SELECT * FROM upsilon_candidates_sp1235;
  -- UNION ALL's

CREATE TEMPORARY VIEW event_features AS
  SELECT * FROM event_level_features_sp1235;
  -- UNION ALL's

EXPLAIN
CREATE TEMPORARY TABLE ml_sample AS 
  SELECT * FROM 
  (ml_sample_meta_cand INNER JOIN candidate_features USING (eid, cidx))
  INNER JOIN 
  event_features USING (eid);
