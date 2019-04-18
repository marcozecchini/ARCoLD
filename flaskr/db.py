import sqlite3
import multiprocessing
import click
from flask import current_app, g
from flask.cli import with_appcontext

cage_id = multiprocessing.Value('i', 2) # 1 already in the db
lick_id = multiprocessing.Value('i', 1)
prog_id = multiprocessing.Value('i', 1)

def get_db():
    if 'db' not in g:
		g.db = sqlite3.connect(
			current_app.config['DATABASE'],
			detect_types=sqlite3.PARSE_DECLTYPES)
		g.db.row_factory = sqlite3.Row
	return g.db

@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    with current_app.open_resource('schema.sql', mode='r') as f:
		db.cursor().executescript(f.read().decode('utf8'))
        
        
@click.command('init-db')
@with_appcontext
def init_db_command():
	init_db()
	click.echo('Initialized the database')
	
def init_app(app):
	app.teardown_appcontext(close_db)
	app.cli.add_command(install)
	
def insert_cage(name):
	import sqlite3 
	conn = sqlite3.connect('arcold.db')
	cursor = conn.cursor()
	
	cursor.executescript('''INSERT INTO cages VALUES ({0}, {1})'''.format(cage_id.value, name))
	cage_id.value += 1
	conn.commit()
	conn.close()
	
def insert_licking_events(start_time, final_time, cage_id):
	import sqlite3 
	conn = sqlite3.connect('arcold.db')
	cursor = conn.cursor()
	
	cursor.executescript('''INSERT INTO licking_events VALUES ({0}, {1}, {2}, {3})'''.format(lick_id.value, start_time, final_time, cage_id))
	lick_id.value += 1
	conn.commit()
	conn.close()
	
def insert_program_events(start_time, final_time, cage_id):
	import sqlite3 
	conn = sqlite3.connect('arcold.db')
	cursor = conn.cursor()
	
	cursor.executescript('''INSERT INTO program_events VALUES ({0}, {1}, {2}, {3})'''.format(prog_id.value, start_time, final_time, cage_id))
	prog_id.value += 1
	conn.commit()
	conn.close()

def licking_event_selection_counter(id):
	from datetime import datetime
	conn = sqlite3.connect('arcold.db')
	cursor = conn.cursor()
	day_ago = datetime.now().timestamp() - 3600*24
	
	cursor.execute(''' SELECT count * FROM licking_events l WHERE l.final_time > {0} AND  l.cage_id == {1}'''.format(day_ago, id))
	res = cursor.fetchone()
	conn.close()
	return res
