from flask import Blueprint, render_template, request, url_for, redirect, flash

from .extensions import db
from .models import URL

shorten = Blueprint('shorten', __name__)

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
def add_link():
	# Create a new database object with a request from the user
	user_request   = request.form['original_url']
	shortened_link = URL(original_url = user_request)

	# Add to database
	db.session.add(shortened_link)
	db.session.commit()

	return render_template('success.html', new_link = shortened_link.short_url, original_url = shortened_link.original_url)

@shorten.route('/stats')
def stats():
	# Send all db entries to stats
	all_links = URL.query.all()
	return render_template("link_stats.html", stats = all_links)

# Route for page not found
@shorten.errorhandler(404)
def page_not_found(e):
	return 'not found 404', 404