from flask import Blueprint, render_template, request, url_for, redirect, flash, session
from functools import wraps

from .extensions import db
from .models import URL, User

shorten = Blueprint('shorten', __name__)

#decorator for login
def login_required(func):
	@wraps(func)
	def wrap(*args, **kwargs):
		if session["USERNAME"]:
			return func(*args, **kwargs)
		else:
			flash("Login first.")
			return redirect(url_for('shorten.login'))
	return wrap

# Route for handling the login page logic
@shorten.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
    	username = request.form['username']
    	user = User.query.filter_by(email = username).first()

    	if not user:
        	error = 'User does not exist. Please sign up'
    	else:
        	password = request.form['password']
        	if user.password != password:
        		error = "Invalid password. Please try again"
        	else:
        		session["USERNAME"] = username
        		return redirect(url_for('shorten.index'))

        
    return render_template('login.html', error=error)

@shorten.route('/signup', methods=['GET', 'POST'])
def signup():
    status = None
    if request.method == 'POST':
    	username = request.form['username']
    	# Check to see if user exists
    	user = User.query.filter_by(email = username).first()
    	if user:
        	status = 'User exists. Please log in.'
    	else:
        	password = request.form['password']
        	new_user = User(email = username, password= password)
        	db.session.add(new_user)
        	db.session.commit()

        	status = "Successfully added user."

        
    return render_template('signup.html', status=status)

@shorten.route('/<short_url>')
def redirect_to_original(short_url):
	# Find the link to redirect to. If not found, return 404
	redirect_link 		  = URL.query.filter_by(short_url = short_url).first_or_404()
	# Add 1 to link visits
	redirect_link.visits += 1
	# Commit to database
	db.session.commit()

	return redirect(redirect_link.original_url)

@shorten.route('/')
@login_required
def index():
	# Main page
	return render_template('index.html')

@shorten.route('/delete/<short_url>')
def delete(short_url):
	# Main page
	link_to_delete = URL.query.filter_by(short_url = short_url).first()

	if not link_to_delete:
		flash("No such link found")
	else:
		db.session.delete(link_to_delete)
		db.session.commit()
		flash("Link successfully deleted")

	all_links = URL.query.all()
	return redirect(url_for('shorten.stats'))
	

@shorten.route('/add_link', methods = ['POST'])
@login_required
def add_link():
	# Create a new database object with a request from the user
	user_request   = request.form['original_url']
	shortened_link = URL(original_url = user_request, creator = User.query.filter_by(email = session.get("USERNAME")).first())

	# Add to database
	db.session.add(shortened_link)
	db.session.commit()

	return render_template('success.html', new_link = shortened_link.short_url, original_url = shortened_link.original_url)

@shorten.route('/logout')
@login_required
def logout():
	session.clear()
	return redirect(url_for('shorten.login'))

@shorten.route('/stats')
@login_required
def stats():
	# Send all db entries to stats
	print(session.get("USERNAME"))
	all_links = URL.query.filter_by(creator_id = session.get("USERNAME")).all()
	return render_template("link_stats.html", stats = all_links)

# Route for page not found
@shorten.errorhandler(404)
def page_not_found(e):
	return 'not found 404', 404