# imports
from flask import Flask, render_template, flash, request, url_for, redirect, session, g
from flask_mysqldb import MySQL
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import os, gc
from functools import wraps

from FlaskApp.tasks import degiro_uploader

from . import db, degiro
from .forms import TransactionsForm, UploadFile

import redis

BASE_CURRENCY='EUR'


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
			c.execute("SELECT * FROM fx_rates ORDER BY date_col DESC LIMIT 1")
			rate = c.fetchone()['EURUSD']
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
				flash("You are now logged in.", "success")
				c.close()
				conn.close()
				return redirect(url_for('index'))

			flash(error, "warning")
	
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
				
				flash(error, "warning")
			except Exception as e:
				return str(e)

		return render_template('register.html')
	

	@app.route('/logout/')
	@login_required
	def logout():
		session.clear()
		flash("You have been logged out.", "success")
		return redirect(url_for('index'))

	@app.route('/transactions/')
	@login_required
	def transactions():
		form = TransactionsForm()
		upload_form = UploadFile()
		return render_template('transactions.html', form=form, upload_form=upload_form)

	@app.route('/add', methods=['POST'])
	@login_required
	def add():
		form = TransactionsForm()
		upload_form = UploadFile()
		if request.method == "POST":
			c, conn = db.connection()
			user_id =session.get('user_id')
			asset_type = form.asset_type.data
			if form.units.data:
				units = form.units.data
			else:
				units = 1 
			if form.buy_sell.data == "Sell":
				units *= -1
			date = form.date.data
			
			if asset_type =='Gold':
				name = ''.join([asset_type,'.',form.symbol.data])
				symbol = name.upper()
			else:
				symbol = form.symbol.data
				name = form.name.data
			price = form.price.data
			currency = form.currency.data
			
			if form.fx_rate.data is not None:
				fx_rate = form.fx_rate.data
			else:
				if BASE_CURRENCY != currency:
					x= c.execute("SELECT * from fx_rates WHERE date_col=%s",(date,))
					conversion = ''.join([BASE_CURRENCY,currency])
					fx_rate = c.fetchone()[conversion]
				else:
					fx_rate = 1
			fee = form.fee.data if form.fee.data else 0

			
			c.execute("INSERT INTO transactions (user_id,asset_type, date_col, symbol, name, units,price,currency,fx_rate,fee) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
				(user_id, asset_type, date, symbol, name, units, price, currency,fx_rate,fee)
				)
			conn.commit()
			c.close()
			conn.close()
			gc.collect()
			flash("Transaction added succesfully.", "success")
			return redirect(url_for('transactions'))

		return render_template('transactions.html', form=form, upload_form=upload_form)
		
	@app.route('/upload', methods=['POST'])
	@login_required
	def upload():
		form = TransactionsForm()
		upload_form = UploadFile()
		if upload_form.validate_on_submit():
			f = upload_form.file.data.stream.readline().decode()
			if  not degiro.validate_csv(f):
				flash("Not a valid format.", "warning")
				return redirect(url_for('transactions'))
			else:
				upload_form.file.data.stream.seek(0)
				user_id=session.get('user_id')
				account_currency = upload_form.account_currency.data
				filename = secure_filename(upload_form.file.data.filename)

				if not os.path.isdir(os.path.join(app.instance_path, str(user_id))):
					os.mkdir(os.path.join(app.instance_path, str(user_id)))

				path = os.path.join(app.instance_path, str(user_id), filename)
				upload_form.file.data.save(path)
				degiro_uploader.delay(user_id,path, account_currency=account_currency)
				flash("File uploaded succesfully. Processing may take a few minutes.","success")
				return redirect(url_for('transactions'))
		else:
			flash("Invalid form. Only CSV allowed", "warning")
			return redirect(url_for('transactions'))


	@app.route('/history', methods=['GET', 'POST'])
	@app.route('/history/<action>/<transaction_id>', methods =['GET', 'POST'])
	@login_required
	def history(action=None, transaction_id=None):
		user_id = session.get('user_id')
		if request.method == "POST":
			if action == 'delete':
				c,conn = db.connection()
				c.execute("DELETE FROM transactions WHERE user_id =%s and id = %s",(user_id, transaction_id))
				conn.commit()
				conn.close()
				flash("Selected transaction was deleted successfully.",'success')
				return redirect(url_for('history'))
		
		elif request.method == "GET":
			c,conn = db.connection()
			x =c.execute('SELECT * FROM transactions WHERE user_id = %s ORDER BY date_col',(user_id,))
			if x > 0:
				transactions = c.fetchall()
			else:
				transactions = None
			conn.close()
		# return transactions[0]
			return render_template('history.html', transactions=transactions)


	@app.route('/portfolio')
	@login_required
	def portfolio():
		user_id=session.get('user_id')
		c,conn = db.connection()
		sql = """SELECT t2.asset_type, concat(IFNULL(t2.symbol,''), IF(exchanges.yahoo is null,'','.') , IFNULL(exchanges.yahoo,'')) as symbol, t2.name, t2.currency, t2.units, t2.Total*-1 as total FROM 
(SELECT ANY_VALUE(asset_type) as asset_type, symbol,ANY_VALUE(exchange) as exchange, ANY_VALUE(name) as name, ANY_VALUE(currency) as currency, sum(units) as units, sum(value)as Total FROM (SELECT *, (units*price/(fx_rate*-1)+fee) AS value from transactions where user_id =%s) t1 GROUP BY symbol) t2 
LEFT JOIN exchanges ON t2.exchange = exchanges.mic
WHERE units>0 ORDER BY total DESC;"""

		x =c.execute(sql,(user_id,))
		if x > 0:
			transactions = c.fetchall()
		else:
			transactions = None
		conn.close()
		r =redis.Redis()
		for item in transactions:
				item['price'] = round(float(r.get(item['symbol']).decode()),2) if r.get(item['symbol']) else None
		
		return render_template('portfolio.html', transactions=transactions, base=BASE_CURRENCY)

	return app






