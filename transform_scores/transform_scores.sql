-- generic
BEGIN; 

CREATE MATERIALIZED VIEW candidate_optimized_events_scores_generic_t AS 
SELECT 
  eid, 

  logre_signal_score,
  gbdt300_signal_score,
  logre_dstartau_score,
  gbdt300_dstartau_score,

  CASE WHEN logre_signal_score=1 THEN NULL
       WHEN logre_signal_score=0 THEN NULL
       ELSE log(logre_signal_score/(1-logre_signal_score)) 
  END AS logit_logre_signal_score,

  CASE WHEN gbdt300_signal_score=1 THEN NULL
       WHEN gbdt300_signal_score=0 THEN NULL
       ELSE log(gbdt300_signal_score/(1-gbdt300_signal_score)) 
  END AS logit_gbdt300_signal_score,

  CASE WHEN logre_dstartau_score=1 THEN NULL
       WHEN logre_dstartau_score=0 THEN NULL
       ELSE log(logre_dstartau_score/(1-logre_dstartau_score)) 
  END AS logit_logre_dstartau_score,

  CASE WHEN gbdt300_dstartau_score=1 THEN NULL
       WHEN gbdt300_dstartau_score=0 THEN NULL
       ELSE log(gbdt300_dstartau_score/(1-gbdt300_dstartau_score)) 
  END AS logit_gbdt300_dstartau_score

FROM candidate_optimized_events_scores_generic;

CREATE INDEX ON candidate_optimized_events_scores_generic_t (eid);

COMMIT;

VACUUM ANALYZE candidate_optimized_events_scores_generic_t;


-- sigmc

BEGIN; 

CREATE MATERIALIZED VIEW candidate_optimized_events_scores_sigmc_t AS 
SELECT 
  eid, 

  logre_signal_score,
  gbdt300_signal_score,
  logre_dstartau_score,
  gbdt300_dstartau_score,

  CASE WHEN logre_signal_score=1 THEN NULL
       WHEN logre_signal_score=0 THEN NULL
       ELSE log(logre_signal_score/(1-logre_signal_score)) 
  END AS logit_logre_signal_score,

  CASE WHEN gbdt300_signal_score=1 THEN NULL
       WHEN gbdt300_signal_score=0 THEN NULL
       ELSE log(gbdt300_signal_score/(1-gbdt300_signal_score)) 
  END AS logit_gbdt300_signal_score,

  CASE WHEN logre_dstartau_score=1 THEN NULL
       WHEN logre_dstartau_score=0 THEN NULL
       ELSE log(logre_dstartau_score/(1-logre_dstartau_score)) 
  END AS logit_logre_dstartau_score,

  CASE WHEN gbdt300_dstartau_score=1 THEN NULL
       WHEN gbdt300_dstartau_score=0 THEN NULL
       ELSE log(gbdt300_dstartau_score/(1-gbdt300_dstartau_score)) 
  END AS logit_gbdt300_dstartau_score

FROM candidate_optimized_events_scores_sigmc;

CREATE INDEX ON candidate_optimized_events_scores_sigmc_t (eid);

COMMIT;

VACUUM ANALYZE candidate_optimized_events_scores_sigmc_t;


-- data

BEGIN; 

CREATE MATERIALIZED VIEW candidate_optimized_events_scores_data_t AS 
SELECT 
  eid, 

  logre_signal_score,
  gbdt300_signal_score,
  logre_dstartau_score,
  gbdt300_dstartau_score,

  CASE WHEN logre_signal_score=1 THEN NULL
       WHEN logre_signal_score=0 THEN NULL
       ELSE log(logre_signal_score/(1-logre_signal_score)) 
  END AS logit_logre_signal_score,

  CASE WHEN gbdt300_signal_score=1 THEN NULL
       WHEN gbdt300_signal_score=0 THEN NULL
       ELSE log(gbdt300_signal_score/(1-gbdt300_signal_score)) 
  END AS logit_gbdt300_signal_score,

  CASE WHEN logre_dstartau_score=1 THEN NULL
       WHEN logre_dstartau_score=0 THEN NULL
       ELSE log(logre_dstartau_score/(1-logre_dstartau_score)) 
  END AS logit_logre_dstartau_score,

  CASE WHEN gbdt300_dstartau_score=1 THEN NULL
       WHEN gbdt300_dstartau_score=0 THEN NULL
       ELSE log(gbdt300_dstartau_score/(1-gbdt300_dstartau_score)) 
  END AS logit_gbdt300_dstartau_score

FROM candidate_optimized_events_scores_data;

CREATE INDEX ON candidate_optimized_events_scores_data_t (eid);

COMMIT;

VACUUM ANALYZE candidate_optimized_events_scores_data_t;
