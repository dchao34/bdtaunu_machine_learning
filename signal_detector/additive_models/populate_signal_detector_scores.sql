BEGIN;

CREATE TABLE signal_detector_scores_generic (
  eid bigint,
  logre_signal_score numeric
);

\copy signal_detector_scores_generic FROM 'signal_detector_scores_generic.csv' WITH CSV HEADER;

CREATE INDEX ON signal_detector_scores_generic (eid);

DROP VIEW temp_signal_detector_inputs_generic;

COMMIT;

VACUUM ANALYZE signal_detector_scores_generic;
