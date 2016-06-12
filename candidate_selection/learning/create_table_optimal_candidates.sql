
-- data

BEGIN;

CREATE TEMPORARY VIEW candrank_data AS 
SELECT 
  eid, 
  cidx, 
  rank() OVER (PARTITION BY eid ORDER BY cand_score DESC, cidx DESC)
FROM 
  upsilon_candidates_data;

CREATE TABLE optimal_upsilon_candidates_data AS 
SELECT eid, cidx FROM candrank_data WHERE rank=1;

CREATE INDEX ON optimal_upsilon_candidates_data (eid);

COMMIT;

VACUUM ANALYZE optimal_upsilon_candidates_data;


-- sigmc
BEGIN;

CREATE TEMPORARY VIEW candrank_sigmc AS 
SELECT 
  eid, 
  cidx, 
  rank() OVER (PARTITION BY eid ORDER BY cand_score DESC, cidx DESC)
FROM 
  upsilon_candidates_sigmc;

CREATE TABLE optimal_upsilon_candidates_sigmc AS 
SELECT eid, cidx FROM candrank_sigmc WHERE rank=1;

CREATE INDEX ON optimal_upsilon_candidates_sigmc (eid);

COMMIT;

VACUUM ANALYZE optimal_upsilon_candidates_sigmc;


-- generic
BEGIN;

CREATE TEMPORARY VIEW candrank_sp1235 AS 
SELECT 
  eid, 
  cidx, 
  rank() OVER (PARTITION BY eid ORDER BY cand_score DESC, cidx DESC)
FROM 
  upsilon_candidates_sp1235;

CREATE TEMPORARY VIEW candrank_sp1237 AS 
SELECT 
  eid, 
  cidx, 
  rank() OVER (PARTITION BY eid ORDER BY cand_score DESC, cidx DESC)
FROM 
  upsilon_candidates_sp1237;

CREATE TEMPORARY VIEW candrank_sp1005 AS 
SELECT 
  eid, 
  cidx, 
  rank() OVER (PARTITION BY eid ORDER BY cand_score DESC, cidx DESC)
FROM 
  upsilon_candidates_sp1005;

CREATE TEMPORARY VIEW candrank_sp998 AS 
SELECT 
  eid, 
  cidx, 
  rank() OVER (PARTITION BY eid ORDER BY cand_score DESC, cidx DESC)
FROM 
  upsilon_candidates_sp998;

CREATE TEMPORARY VIEW candrank_generic AS
SELECT eid, cidx FROM 
  (SELECT * FROM candrank_sp1235 WHERE rank=1 UNION ALL
   SELECT * FROM candrank_sp1237 WHERE rank=1 UNION ALL
   SELECT * FROM candrank_sp1005 WHERE rank=1 UNION ALL
   SELECT * FROM candrank_sp998 WHERE rank=1) AS Q;

CREATE TABLE optimal_upsilon_candidates_generic AS 
SELECT * FROM candrank_generic;

CREATE INDEX ON optimal_upsilon_candidates_generic (eid);

COMMIT;

VACUUM ANALYZE optimal_upsilon_candidates_generic;

