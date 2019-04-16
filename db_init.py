import sqlite3

conn = sqlite3.connect('arcold.db')
cursor = conn.cursor()

cursor.executescript(''' CREATE TABLE IF NOT EXISTS cages 
					(id int PRIMARY KEY, 
					name varchar(127) NOT NULL 
					);''')
					
cursor.executescript(''' CREATE TABLE IF NOT EXISTS licking_events 
					(id int PRIMARY KEY,
					 start_time timestamp NOT NULL,
					 final_time timestampo NOT NULL, 
					 cage_id int,
					 FOREIGN KEY (cage_id) REFERENCES cages(id)
					);''')
					
cursor.executescript(''' CREATE TABLE IF NOT EXISTS program_events(
					id int PRIMARY KEY,
					datetime_start timestamp NOT NULL,
					datetime_end timestamp NOT NULL,
					cage_id int,
					FOREIGN KEY (cage_id) REFERENCES cages(id)
					);''')
					
#cursor.execute('''INSERT INTO cages VALUES ('first') ''')					

conn.commit()
conn.close()
