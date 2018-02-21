import json 
import warnings
from math import cos, asin, sqrt




class Location(object):
	def __init__(self, id=None, latitude=60, longitude=60, geometry_id=None):
		self.id = id
		self.latitude = latitude
		self.longitude = longitude
		self.geometry_id = geometry_id

def distance(lat1, lon1, lat2, lon2):
	p = 0.017453292519943295
	a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
	return 12742 * asin(sqrt(a))

def closest(data, v):
	return min(data, key=lambda p: distance(v.latitude,v.longitude,p.latitude,p.longitude))

class LocationList(object):
	def __init__(self):
		self.lst_locations = []

	def add_object(self, obj):
		if isinstance(obj, Location):
			self.lst_locations.append(obj)
		else:
			print('Type is not supported')

	def find_nearest(self, location):
		if isinstance(location, Location):
			return closest(self.lst_locations, location)
		else:
			print('Type is not supported')



def parse_locations(data):
	lst = LocationList()
	for l in data['result']['items']:
		obj = Location(id=l['id'],
					   latitude=l['lat'],
					   longitude=l['lon'],
					   geometry_id=l['geometry_id'])
		lst.add_object(obj)
	return lst




def get_nearest_location(latitude=60, longitude=40, bank_or_atm='bank'):
	if bank_or_atm == 'bank':
		file_location = './data/otdeleniya.json'
	elif bank_or_atm == 'atm':
		file_location = './data/bankomat.json'
	else: return None

	with open(file_location) as data_file:    
		data = json.load(data_file)
	lst = parse_locations(data)
	usr_point = Location(latitude=latitude, longitude=longitude)
	nearest_point = lst.find_nearest(usr_point)
	
	return nearest_point.latitude, nearest_point.longitude
