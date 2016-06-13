BEGIN;

CREATE TEMPORARY TABLE event_weights_generic AS
  SELECT *, random() FROM event_weights_sp1235 UNION ALL
  SELECT *, random() FROM event_weights_sp1237 UNION ALL
  SELECT *, random() FROM event_weights_sp1005 UNION ALL
  SELECT *, random() FROM event_weights_sp998;
CREATE INDEX ON event_weights_generic (eid);

CREATE TABLE sample_assignments_generic AS
SELECT eid, 6 AS sample_type FROM event_weights_generic;
CREATE INDEX ON sample_assignments_generic (eid);

CREATE TEMPORARY TABLE random_numbers AS
SELECT eid, random() FROM sample_assignments_generic;
CREATE INDEX ON random_numbers (eid);

UPDATE sample_assignments_generic AS S
SET sample_type = 4
FROM random_numbers AS G
WHERE S.eid=G.eid AND G.random < 0.15;

UPDATE sample_assignments_generic AS S
SET sample_type = 3
FROM random_numbers AS G
WHERE S.eid=G.eid AND G.random < 0.12;

UPDATE sample_assignments_generic AS S
SET sample_type = 2
FROM random_numbers AS G
WHERE S.eid=G.eid AND G.random < 0.09;

UPDATE sample_assignments_generic AS S
SET sample_type = 1
FROM random_numbers AS G
WHERE S.eid=G.eid AND G.random < 0.06;

UPDATE sample_assignments_generic AS S
SET sample_type = 5
FROM event_weights_generic AS G
WHERE S.eid=G.eid AND G.random < G.weight;

COMMIT;

VACUUM ANALYZE sample_assignments_generic;
