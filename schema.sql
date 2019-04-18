CREATE TABLE IF NOT EXISTS cages (id int PRIMARY KEY,
								  name_cage varchar(127) NOT NULL);

CREATE TABLE IF NOT EXISTS licking_events (id int PRIMARY KEY,
					 start_time timestamp NOT NULL,
					 final_time timestamp NOT NULL,
					 cage_id int,
					 FOREIGN KEY (cage_id) REFERENCES cages(id));

CREATE TABLE IF NOT EXISTS program_events(
					id int PRIMARY KEY,
					datetime_start timestamp NOT NULL,
					datetime_end timestamp NOT NULL,
					cage_id int,
					FOREIGN KEY (cage_id) REFERENCES cages(id));
