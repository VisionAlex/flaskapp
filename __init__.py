# imports
from flask import Flask,render_template, url_for

#app init
app = Flask(__name__)


#web pages

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

if __name__ == '__main__':
	app.run(debug=True)
