BEGIN;

CREATE TABLE sample_assignments_sigmc AS 
  SELECT eid FROM framework_ntuples_sigmc;

ALTER TABLE sample_assignments_sigmc 
  ADD COLUMN sample_type integer DEFAULT -1;
ALTER TABLE sample_assignments_sigmc 
  ALTER sample_type DROP DEFAULT;

COMMIT;
