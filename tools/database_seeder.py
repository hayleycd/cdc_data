# this is my database seeder. 

import model

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
		current_file = "../data_from_wonder/" + file
		seed_from_file(current_file)

