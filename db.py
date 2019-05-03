import sqlite3
import multiprocessing
import click
from flask import current_app, g, Flask
from werkzeug.exceptions import abort
from flask.cli import with_appcontext

app = Flask(__name__)

cage_id = multiprocessing.Value('i', 2)  # 1 already in the db
lick_id = multiprocessing.Value('i', 1)
prog_id = multiprocessing.Value('i', 1)


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            'arcold.db',
            detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())


@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def insert_cage(name):
    import sqlite3
    conn = sqlite3.connect('arcold.db')
    cursor = conn.cursor()

    cursor.executescript('''INSERT INTO cages(name) VALUES ({0})'''.format(name))
    cage_id.value += 1
    conn.commit()
    conn.close()


def insert_licking_events(start_time, final_time, cage_id):
    import sqlite3
    conn = sqlite3.connect('arcold.db')
    cursor = conn.cursor()

    cursor.executescript(
        '''INSERT INTO licking_events(start_time, final_time, cage_id) VALUES ({0}, {1}, {2})'''.format(start_time, final_time,
                                                                            cage_id))
    lick_id.value += 1
    conn.commit()
    conn.close()


def insert_program_events(start_time, final_time, cage_id):
    import sqlite3
    conn = sqlite3.connect('arcold.db')
    cursor = conn.cursor()

    cursor.executescript(
        '''INSERT INTO program_events(datetime_start, datetime_end, cage_id) VALUES ({0}, {1}, {2})'''.format(start_time, final_time,
                                                                            cage_id))
    prog_id.value += 1
    conn.commit()
    conn.close()


def licking_event_selection_counter(id):
    from datetime import datetime
    conn = sqlite3.connect('arcold.db')
    cursor = conn.cursor()
    day_ago = datetime.now().timestamp() - 3600 * 24

    cursor.execute(
        ''' SELECT count(*) FROM licking_events WHERE licking_events.final_time > {0} AND  licking_events.cage_id == {1}'''.format(day_ago, id))
    res = cursor.fetchone()
    conn.close()
    return res


def licking_event_selection(id):
    from datetime import datetime
    conn = sqlite3.connect('arcold.db')
    cursor = conn.cursor()
    day_ago = datetime.now().timestamp() - 3600 * 24

    cursor.execute(
        ''' SELECT * FROM licking_events WHERE licking_events.final_time > {0} AND  licking_events.cage_id == {1}'''.format(day_ago, id))
    res = cursor.fetchall()
    conn.close()
    return res

def cant_drink(id):
    from datetime import datetime
    conn = sqlite3.connect('arcold.db')
    cursor = conn.cursor()
    now = datetime.now().timestamp()

    cursor.execute(
        ''' SELECT * FROM program_events WHERE program_events.datetime_end > {0} AND program_events.datetime_start < {0} AND  program_events.cage_id == {1}'''.format(now, id))
    res = cursor.fetchone()
    conn.close()
    return res, len(res) > 0 if res is not None else False

def get_cage(id):
    from datetime import datetime
    cage = get_db().execute(
        '''SELECT * FROM cages WHERE id={0}'''.format(id)
    ).fetchone()
    if cage is None:
        abort(404, "Cage id {0} doesn't exist.".format(id))

    return cage

def get_next_prog(cage_id):
    prog_event = get_db().execute(
        '''SELECT * FROM licking_events WHERE cage_id={0} ORDER BY start_time'''.format(cage_id)
    ).fetchall()

    if prog_event is None:
        return None

    return prog_event

def look_for_cage(name):
    cages = get_db().execute(
        '''SELECT * FROM cages '''
    ).fetchall()

    for cage in cages:
        if cage[1] == name:
            return cage[0]

    insert_cage(name)
    return cage_id.value
