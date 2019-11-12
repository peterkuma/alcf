import os
import ds_format as ds
import numpy as np
import aquarius_time as aq
from alcf.lidars import LIDARS

def read_time_periods(filename):
	tp = []
	with open(filename, 'r') as f:
		for line in f.readlines():
			if line.strip() == '':
				continue
			s1, s2 = line.split()
			start = aq.from_iso(s1)
			end = aq.from_iso(s2)
			tp.append([start, end])
	return tp

def run(type_, time_periods, input_, output, eta=0.7):
	"""
alcf calibrate - calibrate ALC backscatter

Calibration based the O'Connor et al. (2004) method of lidar ratio (LR) in fully
opaque stratocumulus clouds.

Usage: `alcf calibrate <type> <time_periods> <input> <output> [<options>]`

- `type`: lidar type (see Types below)
- `time_periods`: file containing calibration time periods of stratocumulus
    clouds in the backscatter profiles (see Time periods below)
- `input`: input directory containing NetCDF files (the output of `alcf lidar`)
- `output`: output calibration file
- `options`: see Options below.

Types:

- `chm15k`: Lufft CHM 15k
- `cl31`: Vaisala CL31
- `cl51`: Vaisala CL51
- `minimpl`: Sigma Space MiniMPL
- `mpl`: Sigma Space MPL

Time periods file:

A text file containting start and end time (see Time format below) of a time
period separated by whitespace, one time period per line:

```
<start> <end>
<start> <end>
...
```

where `start` is the start time and `end` is the end time.

Time format:

"YYYY-MM-DD[THH:MM[:SS]]", where YYYY is year, MM is month, DD is day,
HH is hour, MM is minute, SS is second. Example: 2000-01-01T00:00:00.

Examples:

`alcf calibrate time_periods.txt lidar calibration.txt`

Read time periods from `time_periods.txt`, lidar profiles from the directory
`lidar` and write the calibration coefficient to `calibration.txt`.

	"""
	lidar = LIDARS.get(type_)
	tp = read_time_periods(time_periods)
	files = os.listdir(input_)
	lr = []
	for file in sorted(files):
		filename = os.path.join(input_, file)
		print('<- %s' % filename)
		d = ds.read(filename, ['time'])
		mask = np.zeros(len(d['time']), dtype=np.bool)
		for period in tp:
			mask |= (d['time'] >= period[0]) & \
				(d['time'] < period[1])
		d = ds.read(filename, ['lr'], {'time': mask})
		lr.append(d['lr'])
	lr = np.hstack(lr)
	lr_median = np.median(lr)
	calibration_ceoff = lidar.CALIBRATION_COEFF*lr_median/lidar.SC_LR
	print('-> %s' % output)
	with open(output, 'w') as f:
		f.write('lidar: %s wavelength: %d calibration_coeff: %f lr_median: %f\n' % (
			type_,
			lidar.WAVELENGTH,
			calibration_ceoff,
			lr_median,
		))
