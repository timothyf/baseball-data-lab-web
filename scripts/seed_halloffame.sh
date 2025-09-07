psql -d baseball_web_dev <<'SQL'
DROP TABLE IF EXISTS hof_stage;
CREATE TEMP TABLE hof_stage (
  playerid text,
  yearid int,
  votedby text,
  ballots int,
  needed int,
  votes int,
  inducted text,
  category text,
  needed_note text
);

\COPY hof_stage FROM '/Users/timothyfisher/projects/Baseball/baseball-data-lab/baseball_data_lab/data/hall_of_fame.csv' WITH (FORMAT csv, HEADER true);

INSERT INTO hall_of_fame_votes
  (bbref_id, "year", voted_by, ballots, votes_needed, votes, inducted, category, needed_note)
SELECT
  playerid,
  yearid,
  votedby,
  ballots,
  needed,
  votes,
  (inducted ILIKE 'y')::boolean,
  category,
  needed_note
FROM hof_stage;
SQL
