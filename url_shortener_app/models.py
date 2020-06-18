from .extensions import db

# To get all allowable characters
import string

# To choose the string of 7 characters
from random import choices

# For defaults in the Model
from datetime import datetime

class URL(db.Model):
	# Give each request an ID
	id 			 = db.Column(db.Integer, primary_key = True)
	# Original URL to be shortened
	original_url = db.Column(db.String(512))
	# Shortened URL
	short_url 	 = db.Column(db.String(7), unique = True)
	# How many times a link has been visited, for statistics
	visits 		 = db.Column(db.Integer, default = 0)
	# Time when the link was created. Defaults to current time
	date_created = db.Column(db.DateTime, default = datetime.now)
	# User that created this link
	creator_id	 = db.Column(db.String(32), db.ForeignKey('user.username'))

	# Initializes short URL fora given request.
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.short_url = self.generate_url()

	# Private method to generate a new set of 7 characters for a given entry in the database. 
	# If a given combination of 7 letters exists, generates a new one recursively.
	def generate_url(self):
		# Get all allowable characters
		characters = string.digits + string.ascii_letters
		# Generate url
		short_url  = ''.join(choices(characters, k = 7))

		link = self.query.filter_by(short_url = short_url).first()

		if link: 
			return self.generate_url()
		else:
			return short_url

class User(db.Model):
	username 	  = db.Column(db.String(32), primary_key = True)
	password 	  = db.Column(db.String(32))
	authenticated = db.Column(db.Boolean, default = True)
	links 		  = db.relationship('URL', backref = 'creator')

	def is_active(self):
		return True

	def get_id(self):
		return self.username

	def is_authenticated(self):
		return self.authenticated

	def is_anonymous(self):
		return False