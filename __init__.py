# imports
from flask import Flask, render_template, flash, request, url_for, redirect, session
from flask_mysqldb import MySQL
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import Form, StringField, TextAreaField, validators
import os, gc

from . import db




def create_app(test_config=None):
	app = Flask(__name__,instance_relative_config=True)
	if test_config is None:
		app.config.from_pyfile('config.py', silent=True)
	else:
		app.config.from_mapping(test_config)
	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass

	@app.route("/index")
	@app.route("/")
	def index():
			return render_template("index.html")

	@app.route("/login/", methods=['GET', 'POST'])
	def login():
		if request.method == "POST":
			email = request.form['email']
			password = request.form['password']
			c, conn = db.connection()
			error = None
			op = c.execute("SELECT * FROM users WHERE email = %s", (email,))
			data = c.fetchone()
			if int(op) == 0:
				error = "Invalid credentials."
			elif not check_password_hash(data['password'], password):

				error = "Invalid credentials."
			
			if error is None:
				session.clear()
				session['logged_in'] = True
				session['user_id'] =data['uid']
				flash("You are now logged in.")
				c.close()
				conn.close()
				return redirect(url_for('index'))

			flash(error)
	
		return render_template('login.html')

	@app.route("/register/", methods=['GET', 'POST'])
	def register():
		if request.method == 'POST':
			try:
				firstname = request.form['firstname']
				lastname = request.form['lastname']
				email = request.form['email']
				password = request.form['password']
				confirm = request.form['confirm']
				c, conn = db.connection()  #as defined in the db file
				error = None
				x = c.execute("SELECT * FROM users WHERE email = %s", (email,))
				if int(x) > 0:
					error ="Email already registered."

				if error is None:
					sql = "INSERT INTO users (firstname, lastname, email, password) VALUES (%s, %s, %s, %s)"
					c.execute(sql,(firstname, lastname, email, generate_password_hash(password)))
					conn.commit()
					c.close()
					conn.close()
					gc.collect()

					return redirect(url_for('login'))
				
				flash(error)
			except Exception as e:
				return str(e)

		return render_template('register.html')
	

	@app.route("/test", methods=["GET", "POST"])
	def test():
		if request.method == "POST":
			email = request.form['email']
			password = request.form['password']
			return "succeeded"
		return render_template("test.html")

	
	return app






