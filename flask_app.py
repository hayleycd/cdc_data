# This is my flask_app

from flask import Flask, request, render_template, g, redirect, jsonify
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


if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(debug=True, port=port)