import os, glob
from taiga_reports import tools
from dateutil import parser
from taiga_reports.models.project import Project
from taiga_reports.models.user_story import UserStory
from taiga_reports.models.status import Status
from taiga_reports.snapshot import Snapshot
from taiga_reports.user_report import UserReport

class Report(object):

	def __init__(self, folder):
		directories = [os.path.join(folder,o) for o in os.listdir(folder) if os.path.isdir(os.path.join(folder,o))]
		self._reports = []

		for directory in directories:
			report = Snapshot(directory)
			self._reports.append(report)

		self._reports = sorted(self._reports, key=lambda x: x._datetime)


	def __save_graph(self, filename, function, closed, title=None, user_id=None):
		xs, ys_vals = [], {}
		for snap in self._reports:
			if user_id: snap = UserReport(user_id, snap)

			xs.append( snap._datetime )
			values = getattr(snap, function)(not closed)
			for key, val in values.items():
				if key not in ys_vals.keys(): ys_vals[key]=[]
				ys_vals[key].append(val)
		values = [(key, xs, ys) for key, ys in ys_vals.items()]
		tools.export_graph(filename, values, title=title)


	def save_status_counts_graph(self, filename, closed=False, title=None, user_id=None):
		self.__save_graph(filename, 'status_counts', closed, title, user_id)

	def save_status_points_graph(self, filename, closed=False, title=None, user_id=None):
		self.__save_graph(filename, 'status_points', closed, title, user_id)

	def save_tags_counts_graph(self, filename, closed=False, title=None, user_id=None):
		self.__save_graph(filename, 'tags_counts', closed, title, user_id)

	def save_tags_points_graph(self, filename, closed=False, title=None, user_id=None):
		self.__save_graph(filename, 'tags_points', closed, title, user_id)

	

	@property
	def last_snapshot(self): return self._reports[-1]