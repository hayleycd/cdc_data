# This is my flask_app

from flask import Flask, request, render_template, g, redirect, jsonify
import model
import jinja2
import json
import os
import lat_long_dict
import cases_by_year_loc

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
	lat_lon = lat_long_dict.lat_long_dict
	cases = cases_by_year_loc.cases_by_loc_year_dict

	loc_data = {}

	for key in lat_lon.keys():
		loc_data[key] = {"lat": lat_lon[key]["lat"], "lon": lat_lon[key]["lon"], "cases": cases[key]}


	loc_json = json.dumps(loc_data)

	return loc_json



if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(debug=True, port=port)