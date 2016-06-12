CREATE TEMPORARY TABLE event_weights_generic AS
  SELECT *, random() FROM event_weights_sp1235;
  -- append UNION ALL's
CREATE INDEX ON event_weights_generic (eid);

CREATE TABLE sample_assignment_generic AS
SELECT eid, 6 AS sample_type FROM event_weights_generic;
CREATE INDEX ON sample_assignment_generic (eid);

UPDATE sample_assignment_generic AS S
SET sample_type = 5
FROM event_weights_generic AS G
WHERE S.eid=G.eid AND G.random < G.weight;

CREATE TEMPORARY TABLE random_numbers AS
SELECT eid, random() FROM sample_assignment_generic;
CREATE INDEX ON random_numbers (eid);

UPDATE sample_assignment_generic AS S
SET sample_type = 4
FROM random_numbers AS G
WHERE S.eid=G.eid AND G.random < 0.04;

UPDATE sample_assignment_generic AS S
SET sample_type = 3
FROM random_numbers AS G
WHERE S.eid=G.eid AND G.random < 0.03;

UPDATE sample_assignment_generic AS S
SET sample_type = 2
FROM random_numbers AS G
WHERE S.eid=G.eid AND G.random < 0.02;

UPDATE sample_assignment_generic AS S
SET sample_type = 1
FROM random_numbers AS G
WHERE S.eid=G.eid AND G.random < 0.01;
