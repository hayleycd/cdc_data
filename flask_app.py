# This is my flask_app

from flask import Flask, render_template
import model
import jinja2
import json
import os

# App information
app = Flask(__name__)
app.secret_key = "PRODUCTIONANDTESTINGKEY"
app.jinja_env.undefined = jinja2.StrictUndefined

# Routes begin here

@app.route("/")
def single_page():
	"""This renders the single page of the app."""
	return render_template("home.html")

@app.route("/loc_data")
def get_lat_lon():
	pass



if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(debug=True, port=port)