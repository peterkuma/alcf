META = {
	'clw': {
		'.dims': ['time', 'level'],
		'standard_name': 'mass_fraction_of_cloud_liquid_water_in_air',
		'units': '1',
	},
	'cli': {
		'.dims': ['time', 'level'],
		'standard_name': 'mass_fraction_of_cloud_ice_in_air',
		'units': '1',
	},
	'ps': {
		'.dims': ['time'],
		'standard_name': 'surface_air_pressure',
		'units': 'Pa',
	},
	'pfull': {
		'.dims': ['time', 'level'],
		'standard_name': 'air_pressure',
		'units': 'Pa',
	},
	'zg': {
		'.dims': ['time', 'level'],
		'standard_name': 'geopotential_height',
		'units': 'm',
	},
	'time': {
		'.dims': ['time'],
		'standard_name': 'time',
		'units': 'days since -4712-01-01T12:00',
	},
	'lon': {
		'.dims': ['time'],
		'standard_name': 'longitude',
		'units': 'degrees_east',
	},
	'lat': {
		'.dims': ['time'],
		'standard_name': 'latitude',
		'units': 'degrees_north',
	},
	'ta': {
		'.dims': ['time', 'level'],
		'standard_name': 'air_temperature',
		'units': 'K',
	},
	'clt': {
		'.dims': ['time', 'level'],
		'standard_name': 'cloud_area_fraction',
		'units': '%',
	},
	'orog': {
		'.dims': ['time'],
		'standard_name': 'surface_altitude',
		'units': 'm',
	},
}

import cmip5
import merra2
import amps
import nzcsm

MODELS = {
	'amps': amps,
	#'cmip5': cmip5,
	#'jra55': jra55,
	'merra2': merra2,
	'nzcsm': nzcsm,
}
