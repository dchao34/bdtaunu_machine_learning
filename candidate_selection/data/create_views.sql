CREATE VIEW temp_candidate_selection_weighted_sigmc AS
SELECT 
  eid,
  Q.p,
  Q.r
FROM (SELECT 
        eid, 
        :scale * weight/(SELECT SUM(weight) FROM event_weights_sigmc) AS p,
        random() as r
      FROM event_weights_sigmc) AS Q
WHERE Q.r < Q.p;

CREATE VIEW temp_candidate_selection_weighted_sigmc_specialized AS
SELECT 
  eid
FROM 
  temp_candidate_selection_weighted_sigmc
  INNER JOIN 
  sample_assignments_sigmc USING (eid)
WHERE 
  sample_type = :sample_type;

CREATE VIEW temp_candidate_selection_sigmc_ml_sample AS
SELECT *
FROM 
  temp_candidate_selection_weighted_sigmc_specialized
  INNER JOIN 
  upsilon_candidates_sigmc USING (eid);

