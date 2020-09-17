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

	@app.route("/login/")
	def login():
		return render_template("login.html")

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
					return redirect(url_for('index'))
				
				flash(error)
			except Exception as e:
				return str(e)

		return render_template('register.html')
	@app.route("/test")
	def test():
			return "True"

	
	return app






