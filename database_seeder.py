# this is my database seeder. 

import os
import requests
import json

import model

MAP_API_URL = "https://maps.googleapis.com/maps/api/geocode/json?address="
GEOCODING_API_CREDENTIALS = "&key=" + os.environ["GEOCODING_API"]

INVALID_CITIES_DICT = {
	'"Northeast, pediatric or not in MSA"': {'lat': 45.364130, 'lon': -69.575096},
	'"Midwest, pediatric or not in MSA"': {'lat': 43.241961, 'lon': -97.194262},
	'"South, pediatric or not in MSA"': {'lat': 34.267517, 'lon': -89.278826},
	'"West, pediatric or not in MSA"': {'lat': 41.998493, 'lon': -119.997061},
	'"Territory, pediatric or not in MSA"': {'lat': 26.230983, 'lon': -90.288540},
}

def seed_from_file(myfile):
	f = open(myfile)
	for line in f:
		line = line.strip()
		attributes = line.split("	")
		if len(attributes) !=  11:
			print "There is a problem"
		else:
			entry = model.RawEntry(year_diagnosed = attributes[0],
				year_diagnosed_code = attributes[1], 
				location = attributes[2],
				location_code = attributes[3],
				cases = int(attributes[10])
				)

			model.sqla_session.add(entry)

	model.sqla_session.commit()

def seed_initial_db():
	files_to_load = ["1986_1989.txt",
					 "1990_1993.txt",
					 "1994_1996.txt",
					 "1997_1999.txt",
					 "2000_2002.txt",
					 "pre_1985.txt",]

	for file in files_to_load:
		current_file = "data_from_wonder/" + file
		seed_from_file(current_file)


def clean_city(city_name):
	city_name = city_name.strip()
	clean_name = ""
	for char in city_name:
		clean_name = clean_name + "+" if char == " " else clean_name + char

	return clean_name

def load_city_table():
	for raw in model.sqla_session.query(model.RawEntry).all():
		if raw.location not in INVALID_CITIES_DICT.keys():
			if model.sqla_session.query(model.City).filter_by(name=raw.location.strip('"')).first() == None:
				city = model.City(name = raw.location.strip('"'))
				model.sqla_session.add(city)
				model.sqla_session.commit()

	for city in model.sqla_session.query(model.City).all():
		url = MAP_API_URL + clean_city(city.name) + GEOCODING_API_CREDENTIALS
		content = json.loads(requests.get(url).content)
		city.lat = content["results"][0]['geometry']['location']["lat"]
		city.lon = content["results"][0]['geometry']['location']["lng"]
		model.sqla_session.commit()

def load_invalid_city_data():
	for each in INVALID_CITIES_DICT.keys():
		city = model.City(name = each.strip('"'), lat = INVALID_CITIES_DICT[each]['lat'], lon = INVALID_CITIES_DICT[each]['lon'])
		model.sqla_session.add(city)
	model.sqla_session.commit()

def load_case_in_city_for_year():
	for raw in model.sqla_session.query(model.RawEntry).all():
		city = model.sqla_session.query(model.City).filter_by(name=raw.location.strip('"')).first()
		cases_year_city = model.sqla_session.query(model.CaseYearCity).filter_by(year=raw.year_diagnosed.strip('"')) \
			.filter_by(city=city.id).first()
		if cases_year_city == None:
			cases = model.CaseYearCity(city = city.id, year = raw.year_diagnosed.strip('"'), cases_diagnosed = raw.cases)
			model.sqla_session.add(cases)
			model.sqla_session.commit()
			print cases.city, cases.year, cases.cases_diagnosed
		else:
			cases_year_city.cases_diagnosed = cases_year_city.cases_diagnosed + raw.cases
			model.sqla_session.commit()


def initial_set_up():
	model.create_db()
	seed_initial_db()
	print "Loaded data"
	load_city_table()
	print "City table complete"
	load_invalid_city_data()
	print "Invalid city data loaded"
	load_case_in_city_for_year()
	print "Cases totaled"


