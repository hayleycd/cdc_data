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
			entry = model.Entry(year_diagnosed = attributes[0],
				year_diagnosed_code = attributes[1], 
				location = attributes[2],
				location_code = attributes[3], 
				age_at_diagnosis = attributes[4], 
				age_at_diagnosis_code = attributes[5],
				exposure_category = attributes[6],
				exposure_code = attributes[7],
				sex_and_orientation = attributes[8],
				sex_and_orientation_code = attributes[9],
				cases = int(attributes[10])
				)

			model.sqla_session.add(entry)

	model.sqla_session.commit()
