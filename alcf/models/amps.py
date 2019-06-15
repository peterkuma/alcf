import ds_format as ds
import os
import numpy as np
from alcf.models import META

KAPPA = 0.2854 # Poisson constant for dry air.

VARIABLES = [
	'QCLOUD',
	'QICE',
	'PSFC',
	'P_HYD',
	'P',
	'PB',
	'PHB',
	'PH',
	'HGT',
	'XTIME',
	'XLONG',
	'XLAT',
	'T',
	'T00',
]

GRACE_TIME = 1/24.

def read(dirname, track, warnings=[]):
	dd_index = ds.readdir(dirname, variables=['XTIME'], jd=True)
	start_time = track['time'][0]
	end_time = track['time'][1]
	dd = []
	for d_index in dd_index:
		time = d_index['XTIME'][0]
		filename = d_index['filename']
		if (time >= start_time - GRACE_TIME) & (time <= end_time + GRACE_TIME):
			k = np.argmin(np.abs(track['time'] - time))
			lon0 = track['lon'][k]
			lat0 = track['lat'][k]
			d = ds.read(filename, variables=VARIABLES, sel={'Time': 0})
			lon = np.where(d['XLONG'] < 0., 360. + d['XLONG'], d['XLONG'])
			lat = d['XLAT']
			l = np.argmin((lon - lon0)**2 + (lat - lat0)**2)
			i, j = np.unravel_index(l, lon.shape)
			clw = d['QCLOUD'][:,i,j]
			cli = d['QICE'][:,i,j]
			clt = 100.*np.ones(len(clw), dtype=np.float64)
			ps = d['PSFC'][i,j]
			orog = d['HGT'][i,j]
			pfull = d['PB'][:,i,j] + d['P'][:,i,j]
			zg = (d['PHB'][:,i,j] + d['PH'][:,i,j])/9.81
			zg = 0.5*(zg[1:] + zg[:-1])
			theta = d['T'][:,i,j] + d['T00']
			ta = theta*(pfull/ps)**KAPPA
			newshape3 = [1] + list(clw.shape)
			newshape2 = [1] + list(ps.shape)
			d_new = {
				'clw': clw.reshape(newshape3),
				'cli': cli.reshape(newshape3),
				'ta': ta.reshape(newshape3),
				'clt': clt.reshape(newshape3),
				'pfull': pfull.reshape(newshape3),
				'zg': zg.reshape(newshape3),
				'ps': ps.reshape(newshape2),
				'orog': orog.reshape(newshape2),
				'lon': np.array([lon[i,j]]),
				'lat': np.array([lat[i,j]]),
				'time': np.array([time]),
				'.': META,
			}
			dd.append(d_new)
	d = ds.op.merge(dd, 'time')
	return d
