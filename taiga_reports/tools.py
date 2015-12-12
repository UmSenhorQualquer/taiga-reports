import six, datetime
from matplotlib import colors
from matplotlib import pyplot as plt
from dateutil   import rrule

def default_working_days():
	r  = rrule.rrule(rrule.DAILY,byweekday=[rrule.MO, rrule.TU, rrule.WE, rrule.TH, rrule.FR],dtstart=datetime.date.today())
	rs = rrule.rruleset()
	rs.rrule(r)
	return rs


def generate_graph(values, title=None, fill=False):
	plt.close()
	fig, ax = plt.subplots()
	if title: ax.set_title(title)

	# Add the single letter colors.
	colors_list = list(six.iteritems(colors.cnames))

	with plt.style.context('fivethirtyeight'):
		for (label, xs, ys), color in zip(values, colors_list):
			if fill: 
				plt.stackplot(xs, ys, colors=color, alpha=0.4)
				plt.plot(xs, ys, color=color[0], alpha=0.9, linewidth=1.5, label=label)
			else:
				plt.plot(xs, ys, alpha=0.8,marker='o', color=color[0], label=label)

	fig.autofmt_xdate()
	plt.legend(loc=2)
	plt.grid(True)

	
def export_graph(filename, values, title=None, fill=False):
	generate_graph(values, title, fill)
	plt.savefig(filename)
		

def show_graph(values, title=None):
	generate_graph(values, title)
	plt.show()
	