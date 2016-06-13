CREATE TABLE candidate_optimized_events_scores_generic AS
SELECT eid FROM candidate_optimized_events_generic;

CREATE INDEX ON candidate_optimized_events_scores_generic (eid);
