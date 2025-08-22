
psql -d baseball_web_dev -h localhost  -c "\COPY team_id_infos(mlbam_team_id,abbrev,full_name,location_name,team_name,league,fg_team_id,mlbam_league_id,mlbam_division_id,bref_team_id,retrosheet_team_id,active_from,active_to) FROM '/Users/timothyfisher/projects/Baseball/baseball-data-lab/baseball_data_lab/data/team_id_infos.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');"

psql -d baseball_web_dev -h localhost  -c "\COPY venues(mlbam_id,name,link,active,season) FROM '/Users/timothyfisher/projects/Baseball/baseball-data-lab/baseball_data_lab/data/mlb_venues.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');"

psql -d baseball_web_dev -h localhost  -c "\COPY player_id_infos( key_person,key_uuid,key_mlbam,key_retro,key_bbref,key_bbref_minors,key_fangraphs,key_npb,name_last,name_first,name_given,name_suffix ) FROM '/Users/timothyfisher/projects/Baseball/baseball-data-lab/baseball_data_lab/data/combined_people.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');"