BEGIN;

CREATE TABLE sample_assignments_sigmc (
  eid integer,
  sample_type integer
);

\copy sample_assignments_sigmc FROM 'sigmc_sample_assignments.csv' WITH CSV HEADER;

CREATE INDEX ON sample_assignments_sigmc (eid);

COMMIT;

VACUUM ANALYZE sample_assignments_sigmc;
