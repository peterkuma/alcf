import convert
import model
import cosp
import lidar
import stats
import plot
import plot_stats

CMDS = {
	'convert': convert.run,
	'model': model.run,
	'cosp': cosp.run,
	'lidar': lidar.run,
	'stats': stats.run,
	'plot': plot.run,
	'plot_stats': plot_stats.run,
}
