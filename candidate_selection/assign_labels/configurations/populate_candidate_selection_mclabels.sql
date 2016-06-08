BEGIN;

CREATE TEMPORARY TABLE candidate_selection_mclabels_sigmc (
  eid bigint,
  cidx integer,
  is_matched integer
) ON COMMIT DROP;

\copy candidate_selection_mclabels_sigmc FROM 'candidate_selection_mclabels_sigmc.csv' WITH CSV HEADER;

CREATE INDEX ON candidate_selection_mclabels_sigmc (eid, cidx);

ALTER TABLE upsilon_candidates_sigmc
  ADD COLUMN is_matched integer;

UPDATE upsilon_candidates_sigmc
  SET is_matched = tmp.is_matched
  FROM candidate_selection_mclabels_sigmc AS tmp
  WHERE 
    upsilon_candidates_sigmc.eid=tmp.eid AND 
    upsilon_candidates_sigmc.cidx=tmp.cidx;

COMMIT;

