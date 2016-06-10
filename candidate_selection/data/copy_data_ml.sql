CREATE TEMPORARY VIEW M AS 
SELECT 
  eid,
  cidx,
  mmiss2prime,
  eextra,
  tag_lp3,
  tag_cosby,
  tag_costhetadl,
  tag_dmass,
  tag_deltam,
  tag_costhetadsoft,
  tag_softp3magcm,
  sig_hp3,
  sig_cosby,
  sig_costhetadtau,
  sig_vtxb,
  sig_dmass,
  sig_deltam,
  sig_costhetadsoft,
  sig_softp3magcm,
  sig_hmass,
  sig_vtxh,
  tag_isbdstar,
  sig_isbdstar,
  tag_dmode,
  tag_dstarmode,
  sig_dmode,
  sig_dstarmode,
  is_matched
FROM 
  temp_candidate_selection_sigmc_ml_sample;

\copy (SELECT * FROM M) TO STDOUT WITH CSV HEADER;
