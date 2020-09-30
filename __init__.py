# imports
from flask import Flask, render_template, flash, request, url_for, redirect, session, g
from flask_mysqldb import MySQL
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import Form, StringField, TextAreaField, validators
import os, gc
from functools import wraps

from . import db
from .forms import TransactionsForm

def login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if g.user is None:
			return redirect(url_for('login'))
		return f(*args, **kwargs)
	return decorated_function





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

	@app.before_request
	def load_logged_in_user():
		user_id= session.get('user_id')

		if user_id is None:
			g.user = None
		else:
			c, conn = db.connection()
			c.execute("SELECT * FROM users WHERE id=%s", (user_id,))
			g.user= c.fetchone()
			c.close()
			conn.close()

	@app.route("/index")
	@app.route("/")
	def index():
			c, conn = db.connection()
			c.execute("SELECT * FROM gold_prices ORDER BY Date DESC LIMIT 1")
			gold = c.fetchone()['Close']
			c.execute("SELECT * FROM fx_rates ORDER BY Date DESC LIMIT 1")
			rate = c.fetchone()['EURUSD=X']
			gold_price = round(gold/rate)
			return render_template("index.html",gold_price=gold_price)

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
				session['user_id'] =data['id']
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
	

	@app.route('/logout/')
	@login_required
	def logout():
		session.clear()
		flash("You have been logged out.")
		return redirect(url_for('index'))

	@app.route('/transactions/', methods=["GET", "POST"])
	@login_required
	def transactions():
		form = TransactionsForm()
		if request.method == "POST":
			user_id =session.get('user_id')
			asset_type = form.asset_type.data
			if form.buy_sell.data == "Buy":
				units = form.units.data
			else:
				units = -form.units.data
			date = form.date.data
			symbol = form.symbol.data
			name = form.name.data
			price = form.price.data
			currency = form.currency.data
			c, conn = db.connection()
			c.execute("INSERT INTO transactions (user_id,asset_type, date, symbol, name, units,price,currency) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
				(user_id, asset_type, date, symbol, name, units, price, currency)
				)
			conn.commit()
			c.close()
			conn.close()
			gc.collect()
			flash("Transaction added succesfully.")
			return redirect(url_for('transactions'))

			return form.data
		return render_template('transactions.html', form=form)
	

	return app






