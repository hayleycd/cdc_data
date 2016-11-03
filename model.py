# This is my model file. My class definitions, reused functions, 
# etc. will live here. 

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Float, Text, Boolean
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey

ENGINE = create_engine("sqlite:///publichealth.db", echo=False)
sqla_session = scoped_session(sessionmaker(bind=ENGINE, autocommit = False, autoflush = False))

Base = declarative_base()
Base.query = sqla_session.query_property()


#
# Classes
#

class RawEntry(Base):

	__tablename__ = "raw_entries"

	id = Column(Integer, primary_key = True)
	year_diagnosed = Column(String(100))
	year_diagnosed_code = Column(Integer)
	location = Column(String(200))
	location_code = Column(String(100))
	age_at_diagnosis = Column(String(100))
	age_at_diagnosis_code = Column(String(100))
	exposure_category = Column(String(200))
	exposure_code = Column(String(100))
	sex_and_orientation = Column(String(200))
	sex_and_orientation_code = Column(String(100))
	cases = Column(Integer)

# functions

def create_db():
	"""Recreates the database."""

	Base.metadata.create_all(ENGINE)

