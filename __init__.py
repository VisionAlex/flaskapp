# imports
from flask import Flask,render_template, url_for
import os

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

	@app.route("/register/")
	def register():
		return render_template('register.html')
	
	return app




