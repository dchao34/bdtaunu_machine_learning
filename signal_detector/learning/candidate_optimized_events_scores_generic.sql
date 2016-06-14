-- generic
BEGIN;

CREATE TABLE candidate_optimized_events_scores_generic AS
SELECT eid FROM candidate_optimized_events_generic;
CREATE INDEX ON candidate_optimized_events_scores_generic (eid);

END;

VACUUM ANALYZE candidate_optimized_events_scores_generic;

-- sigmc
BEGIN;

CREATE TABLE candidate_optimized_events_scores_sigmc AS
SELECT eid FROM candidate_optimized_events_sigmc;
CREATE INDEX ON candidate_optimized_events_scores_sigmc (eid);

END;

VACUUM ANALYZE candidate_optimized_events_scores_sigmc;

-- data
BEGIN;

CREATE TABLE candidate_optimized_events_scores_data AS
SELECT eid FROM candidate_optimized_events_data;
CREATE INDEX ON candidate_optimized_events_scores_data (eid);

END;

VACUUM ANALYZE candidate_optimized_events_scores_data;
