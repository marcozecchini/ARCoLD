import os

from flask import Flask

'''
To launch it:

export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
'''

def create_app(test_config=None):
	#create and configure the app
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_mapping(
	    SECRET_KEY = 'arcold-dev',
	    DATABASE=os.path.join(app.instance_path, 'arcold.db'),
	    )
	if test_config is None:
		#load the instance config, if it exists, when not testing
		app.config.from_pyfile('config.py', silent=True)
	else:
		app.config.from_mapping(test_config)
	
	#to initialize the app	
	from . import db
	db.init_app(app)
	
	from . import arcold
	app.register_blueprint(arcold.bp)
	app.add_url_rule('/', endpoint='index')
	
	#ensure the instance folder exists
	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass
	
	
	@app.route('/hello')
	def hello():
		return 'Hello, world!'
	
	return app
