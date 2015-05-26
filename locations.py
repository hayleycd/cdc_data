import os
import requests
import json
import sys


GEOCODING_API= os.environ["GEOCODING_API"]

LOCATIONS = []

def open_and_append_locales(file):
	f = open(file)
	for line in f:
		line = line.strip()
		attributes = line.split("	")
		location = attributes[2].strip('"')
		if location not in LOCATIONS:
			LOCATIONS.append(location)

def collate_locations():
	open_and_append_locales("through_1985.txt")
	open_and_append_locales("1986_1989.txt")
	open_and_append_locales("1990_1993.txt")
	open_and_append_locales("1994_1996.txt")
	open_and_append_locales("1997_1999.txt")
	open_and_append_locales("2000_2002.txt")

	return LOCATIONS

def get_text_file_of_locations(locations):

	f = open("locations.txt", 'w')

	for location in locations:
		f.write(location + "\n")

	f.close()

def build_lat_lon_dict():
	f = open("locations.txt")
	lat_long_dict = {}

	for line in f:
		line = line.strip()
		new_line = ""
		for char in line:
			if char == " ":
				new_line = new_line + "+"
			else:
				new_line = new_line + char

		url = "https://maps.googleapis.com/maps/api/geocode/json?address="
		url = url + new_line + "&key=" + GEOCODING_API

		lat_lon_request = requests.get(url)

		content= json.loads(lat_lon_request.content)
		lat_long_dict[line] = {"lat": content["results"][0]['geometry']['location']["lat"], 
		"lon": content["results"][0]['geometry']['location']["lng"]}

	sys.stdout = open('lat_long_dict.txt', 'w')

	print lat_long_dict





