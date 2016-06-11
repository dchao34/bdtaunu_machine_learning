CREATE TEMPORARY VIEW candrank_sigmc AS 
SELECT 
  eid, 
  cidx, 
  rank() OVER (PARTITION BY eid ORDER BY cand_score DESC, cidx DESC)
FROM 
  upsilon_candidates_sigmc;

CREATE TEMPORARY VIEW candrank_sp1235 AS 
SELECT 
  eid, 
  cidx, 
  rank() OVER (PARTITION BY eid ORDER BY cand_score DESC, cidx DESC)
FROM 
  upsilon_candidates_sp1235;

CREATE TEMPORARY VIEW optcand_all AS
SELECT eid, cidx FROM 
  (SELECT * FROM candrank_sigmc WHERE rank=1 UNION ALL
   SELECT * FROM candrank_sp1235 WHERE rank=1) AS Q;

CREATE TABLE optimal_upsilon_candidates AS 
SELECT * FROM optcand_all;

CREATE INDEX ON optimal_upsilon_candidates (eid);
