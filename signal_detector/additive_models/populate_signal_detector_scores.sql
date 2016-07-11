-- generic

BEGIN;

-- add new columns into the score table
ALTER TABLE candidate_optimized_events_scores_generic
ADD logre_signal_score numeric;

ALTER TABLE candidate_optimized_events_scores_generic
ADD gbdt300_signal_score numeric;

-- copy scores from the csv file into a temporary table
CREATE TEMPORARY TABLE temp_signal_detector_scores_generic (
  eid bigint,
  logre_signal_score numeric,
  gbdt300_signal_score numeric
) ON COMMIT DROP;

\copy temp_signal_detector_scores_generic FROM 'signal_scores_generic.csv' WITH CSV HEADER;

CREATE INDEX ON temp_signal_detector_scores_generic (eid);

-- update scores
UPDATE candidate_optimized_events_scores_generic AS t1
SET 
  logre_signal_score = t2.logre_signal_score, 
  gbdt300_signal_score = t2.gbdt300_signal_score
FROM temp_signal_detector_scores_generic AS t2
WHERE t1.eid = t2.eid;

COMMIT;

VACUUM ANALYZE candidate_optimized_events_scores_generic;




-- data

BEGIN;

-- add new columns into the score table
ALTER TABLE candidate_optimized_events_scores_data
ADD logre_signal_score numeric;

ALTER TABLE candidate_optimized_events_scores_data
ADD gbdt300_signal_score numeric;

-- copy scores from the csv file into a temporary table
CREATE TEMPORARY TABLE temp_signal_detector_scores_data (
  eid bigint,
  logre_signal_score numeric,
  gbdt300_signal_score numeric
) ON COMMIT DROP;

\copy temp_signal_detector_scores_data FROM 'signal_scores_data.csv' WITH CSV HEADER;

CREATE INDEX ON temp_signal_detector_scores_data (eid);

-- update scores
UPDATE candidate_optimized_events_scores_data AS t1
SET 
  logre_signal_score = t2.logre_signal_score, 
  gbdt300_signal_score = t2.gbdt300_signal_score
FROM temp_signal_detector_scores_data AS t2
WHERE t1.eid = t2.eid;

COMMIT;

VACUUM ANALYZE candidate_optimized_events_scores_data;







-- sigmc

BEGIN;

-- add new columns into the score table
ALTER TABLE candidate_optimized_events_scores_sigmc
ADD logre_signal_score numeric;

ALTER TABLE candidate_optimized_events_scores_sigmc
ADD gbdt300_signal_score numeric;

-- copy scores from the csv file into a temporary table
CREATE TEMPORARY TABLE temp_signal_detector_scores_sigmc (
  eid bigint,
  logre_signal_score numeric,
  gbdt300_signal_score numeric
) ON COMMIT DROP;

\copy temp_signal_detector_scores_sigmc FROM 'signal_scores_sigmc.csv' WITH CSV HEADER;

CREATE INDEX ON temp_signal_detector_scores_sigmc (eid);

-- update scores
UPDATE candidate_optimized_events_scores_sigmc AS t1
SET 
  logre_signal_score = t2.logre_signal_score, 
  gbdt300_signal_score = t2.gbdt300_signal_score
FROM temp_signal_detector_scores_sigmc AS t2
WHERE t1.eid = t2.eid;

COMMIT;

VACUUM ANALYZE candidate_optimized_events_scores_sigmc;
