from flask import (Blueprint, flash, g, redirect, render_template, request, url_for)
from werkzeug.exceptions import abort
from flaskr.db import *

bp = Blueprint('arcold', __name__)

@app.route('/')
def index():
	db = get_db()
	cages = db.execute(
		'SELECT c.id, c.name_cage'
		'FROM cages c'
	).fetchall()
	
	return render_template('index.html', cages=cages)
	
def get_cage(id):
	cage = get_db().execute(
		'SELECT c.id, c.name_cage'
		'FROM cages c'
		'WHERE c.id = ?',
		(id,)
		).fetchone()
	if cage is None:
		abort(404, "Cage id {0} doesn't exist.".format(id))
	
	return cage
	
#@bp.route('cage/<int:id>', methods=('GET', 'POST'))
@bp.route('cage/<int:id>')
def cage_details(id):
	cage = get_cage(id)
	
	counter = licking_event_selection_counter(id)
	
	return render_template('cage.html', cage=cage, counter=counter)
