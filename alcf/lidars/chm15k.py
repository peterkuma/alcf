import numpy as np
import ds_format as ds
from alcf.lidars import META

WAVELENGTH = 1064
CALIBRATION_COEFF = 0.2
SURFACE_LIDAR = True
SC_LR = 18.2 # Stratocumulus lidar ratio (O'Connor et al., 2004)

VARS = {
	'backscatter': ['time', 'range', 'beta_raw'],
	'time': ['time'],
	'zfull': ['range', 'altitude'],
}

def read(filename, vars):
	dep_vars = list(set([y for x in vars if x in VARS for y in VARS[x]]))
	d = ds.from_netcdf(
		filename,
		dep_vars,
	)
	dx = {}
	n, m = d['beta_raw'].shape
	if 'time' in vars:
		dx['time'] = d['time']/(24.0*60.0*60.0) + 2416480.5
	if 'backscatter' in vars:
		dx['backscatter'] = d['beta_raw']*1e-11*CALIBRATION_COEFF
	if 'zfull' in vars:
		zfull1 = d['range'] + d['altitude']
		dx['zfull'] = np.tile(zfull1, (n, 1))
	dx['.'] = META
	dx['.'] = {
		x: dx['.'][x]
		for x in vars
		if x in VARS
	}
	return dx
