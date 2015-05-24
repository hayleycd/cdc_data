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

	years = ['"1981"', 
	'"1982"', 
	'"1983"', 
	'"1984"', 
	'"1985"', 
	'"1986"', 
	'"1987"', 
	'"1988"', 
	'"1989"', 
	'"1990"', 
	'"1991"', 
	'"1992"', 
	'"1993"', 
	'"1994"', 
	'"1995"', 
	'"1996"', 
	'"1997"', 
	'"1998"',
	'"1999"', 
	'"2000"', 
	'"2001"', 
	'"2002"' ]
	case_load_dictionary = {}
	total = 0
	for year in years:
		cases = model.sqla_session.query(model.Entry).filter_by(year_diagnosed_code=year).all()
		case_count = 0
		for case in cases:
			case_count = case_count + case.cases
		case_load_dictionary[year] = case_count
		total = total + case_count

	return render_template("home.html", case_load_dictionary = case_load_dictionary, keys = sorted(case_load_dictionary.keys()), total = total)


if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(debug=True, port=port)