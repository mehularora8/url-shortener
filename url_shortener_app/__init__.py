from flask import Flask

from .extensions import db
from .routes import shorten

def create_app(filename = "settings.py"):
	
	app = Flask(__name__)
	app.secret_key = 'secret'

	app.config.from_pyfile(filename)

	db.init_app(app)

	app.register_blueprint(shorten)

	return app